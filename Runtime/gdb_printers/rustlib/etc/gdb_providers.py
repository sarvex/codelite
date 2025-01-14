from sys import version_info

import gdb

if version_info[0] >= 3:
    xrange = range

ZERO_FIELD = "__0"
FIRST_FIELD = "__1"


def unwrap_unique_or_non_null(unique_or_nonnull):
    # BACKCOMPAT: rust 1.32
    # https://github.com/rust-lang/rust/commit/7a0911528058e87d22ea305695f4047572c5e067
    ptr = unique_or_nonnull["pointer"]
    return ptr if ptr.type.code == gdb.TYPE_CODE_PTR else ptr[ZERO_FIELD]


class EnumProvider:
    def __init__(self, valobj):
        content = valobj[valobj.type.fields()[0]]
        fields = content.type.fields()
        self.empty = len(fields) == 0
        if not self.empty:
            discriminant = 0 if len(fields) == 1 else int(content[fields[0]]) + 1
            self.active_variant = content[fields[discriminant]]
            self.name = fields[discriminant].name
            self.full_name = f"{valobj.type.name}::{self.name}"
        else:
            self.full_name = valobj.type.name

    def to_string(self):
        return self.full_name

    def children(self):
        if not self.empty:
            yield self.name, self.active_variant


class StdStringProvider:
    def __init__(self, valobj):
        self.valobj = valobj
        vec = valobj["vec"]
        self.length = int(vec["len"])
        self.data_ptr = unwrap_unique_or_non_null(vec["buf"]["ptr"])

    def to_string(self):
        return self.data_ptr.lazy_string(encoding="utf-8", length=self.length)

    @staticmethod
    def display_hint():
        return "string"


class StdOsStringProvider:
    def __init__(self, valobj):
        self.valobj = valobj
        buf = self.valobj["inner"]["inner"]
        is_windows = "Wtf8Buf" in buf.type.name
        vec = buf[ZERO_FIELD] if is_windows else buf

        self.length = int(vec["len"])
        self.data_ptr = unwrap_unique_or_non_null(vec["buf"]["ptr"])

    def to_string(self):
        return self.data_ptr.lazy_string(encoding="utf-8", length=self.length)

    def display_hint(self):
        return "string"


class StdStrProvider:
    def __init__(self, valobj):
        self.valobj = valobj
        self.length = int(valobj["length"])
        self.data_ptr = valobj["data_ptr"]

    def to_string(self):
        return self.data_ptr.lazy_string(encoding="utf-8", length=self.length)

    @staticmethod
    def display_hint():
        return "string"


class StdVecProvider:
    def __init__(self, valobj):
        self.valobj = valobj
        self.length = int(valobj["len"])
        self.data_ptr = unwrap_unique_or_non_null(valobj["buf"]["ptr"])

    def to_string(self):
        return f"Vec(size={self.length})"

    def children(self):
        saw_inaccessible = False
        for index in xrange(self.length):
            element_ptr = self.data_ptr + index
            if saw_inaccessible:
                return
            try:
                # rust-lang/rust#64343: passing deref expr to `str` allows
                # catching exception on garbage pointer
                str(element_ptr.dereference())
                yield (f"[{index}]", element_ptr.dereference())
            except RuntimeError:
                saw_inaccessible = True
                yield str(index), "inaccessible"

    @staticmethod
    def display_hint():
        return "array"


class StdVecDequeProvider:
    def __init__(self, valobj):
        self.valobj = valobj
        self.head = int(valobj["head"])
        self.tail = int(valobj["tail"])
        self.cap = int(valobj["buf"]["cap"])
        self.data_ptr = unwrap_unique_or_non_null(valobj["buf"]["ptr"])
        if self.head >= self.tail:
            self.size = self.head - self.tail
        else:
            self.size = self.cap + self.head - self.tail

    def to_string(self):
        return f"VecDeque(size={self.size})"

    def children(self):
        for index in xrange(0, self.size):
            value = (self.data_ptr + ((self.tail + index) % self.cap)).dereference()
            yield (f"[{index}]", value)

    @staticmethod
    def display_hint():
        return "array"


class StdRcProvider:
    def __init__(self, valobj, is_atomic=False):
        self.valobj = valobj
        self.is_atomic = is_atomic
        self.ptr = unwrap_unique_or_non_null(valobj["ptr"])
        self.value = self.ptr["data" if is_atomic else "value"]
        self.strong = self.ptr["strong"]["v" if is_atomic else "value"]["value"]
        self.weak = self.ptr["weak"]["v" if is_atomic else "value"]["value"] - 1

    def to_string(self):
        if self.is_atomic:
            return f"Arc(strong={int(self.strong)}, weak={int(self.weak)})"
        else:
            return f"Rc(strong={int(self.strong)}, weak={int(self.weak)})"

    def children(self):
        yield "value", self.value
        yield "strong", self.strong
        yield "weak", self.weak


class StdCellProvider:
    def __init__(self, valobj):
        self.value = valobj["value"]["value"]

    def to_string(self):
        return "Cell"

    def children(self):
        yield "value", self.value


class StdRefProvider:
    def __init__(self, valobj):
        self.value = valobj["value"].dereference()
        self.borrow = valobj["borrow"]["borrow"]["value"]["value"]

    def to_string(self):
        borrow = int(self.borrow)
        return f"Ref(borrow={borrow})" if borrow >= 0 else f"Ref(borrow_mut={-borrow})"

    def children(self):
        yield "*value", self.value
        yield "borrow", self.borrow


class StdRefCellProvider:
    def __init__(self, valobj):
        self.value = valobj["value"]["value"]
        self.borrow = valobj["borrow"]["value"]["value"]

    def to_string(self):
        borrow = int(self.borrow)
        if borrow >= 0:
            return f"RefCell(borrow={borrow})"
        else:
            return f"RefCell(borrow_mut={-borrow})"

    def children(self):
        yield "value", self.value
        yield "borrow", self.borrow


# Yields children (in a provider's sense of the word) for a BTreeMap.
def children_of_btree_map(map):
    # Yields each key/value pair in the node and in any child nodes.
    def children_of_node(node_ptr, height):
        def cast_to_internal(node):
            internal_type_name = node.type.target().name.replace("LeafNode", "InternalNode", 1)
            internal_type = gdb.lookup_type(internal_type_name)
            return node.cast(internal_type.pointer())

        if node_ptr.type.name.startswith("alloc::collections::btree::node::BoxedNode<"):
            # BACKCOMPAT: rust 1.49
            node_ptr = node_ptr["ptr"]
        node_ptr = unwrap_unique_or_non_null(node_ptr)
        leaf = node_ptr.dereference()
        keys = leaf["keys"]
        vals = leaf["vals"]
        edges = cast_to_internal(node_ptr)["edges"] if height > 0 else None
        length = leaf["len"]

        for i in xrange(0, length + 1):
            if height > 0:
                child_ptr = edges[i]["value"]["value"]
                yield from children_of_node(child_ptr, height - 1)
            if i < length:
                # Avoid "Cannot perform pointer math on incomplete type" on zero-sized arrays.
                key_type_size = keys.type.sizeof
                val_type_size = vals.type.sizeof
                key = keys[i]["value"]["value"] if key_type_size > 0 else gdb.parse_and_eval("()")
                val = vals[i]["value"]["value"] if val_type_size > 0 else gdb.parse_and_eval("()")
                yield key, val

    if map["length"] > 0:
        root = map["root"]
        if root.type.name.startswith("core::option::Option<"):
            root = root.cast(gdb.lookup_type(root.type.name[21:-1]))
        node_ptr = root["node"]
        height = root["height"]
        yield from children_of_node(node_ptr, height)


class StdBTreeSetProvider:
    def __init__(self, valobj):
        self.valobj = valobj

    def to_string(self):
        return f'BTreeSet(size={self.valobj["map"]["length"]})'

    def children(self):
        inner_map = self.valobj["map"]
        for i, (child, _) in enumerate(children_of_btree_map(inner_map)):
            yield (f"[{i}]", child)

    @staticmethod
    def display_hint():
        return "array"


class StdBTreeMapProvider:
    def __init__(self, valobj):
        self.valobj = valobj

    def to_string(self):
        return f'BTreeMap(size={self.valobj["length"]})'

    def children(self):
        for i, (key, val) in enumerate(children_of_btree_map(self.valobj)):
            yield (f"key{i}", key)
            yield (f"val{i}", val)

    @staticmethod
    def display_hint():
        return "map"


# BACKCOMPAT: rust 1.35
class StdOldHashMapProvider:
    def __init__(self, valobj, show_values=True):
        self.valobj = valobj
        self.show_values = show_values

        self.table = self.valobj["table"]
        self.size = int(self.table["size"])
        self.hashes = self.table["hashes"]
        self.hash_uint_type = self.hashes.type
        self.hash_uint_size = self.hashes.type.sizeof
        self.modulo = 2 ** self.hash_uint_size
        self.data_ptr = self.hashes[ZERO_FIELD]["pointer"]

        self.capacity_mask = int(self.table["capacity_mask"])
        self.capacity = (self.capacity_mask + 1) % self.modulo

        marker = self.table["marker"].type
        self.pair_type = marker.template_argument(0)
        self.pair_type_size = self.pair_type.sizeof

        self.valid_indices = []
        for idx in range(self.capacity):
            data_ptr = self.data_ptr.cast(self.hash_uint_type.pointer())
            address = data_ptr + idx
            hash_uint = address.dereference()
            hash_ptr = hash_uint[ZERO_FIELD]["pointer"]
            if int(hash_ptr) != 0:
                self.valid_indices.append(idx)

    def to_string(self):
        if self.show_values:
            return f"HashMap(size={self.size})"
        else:
            return f"HashSet(size={self.size})"

    def children(self):
        start = int(self.data_ptr) & ~1

        hashes = self.hash_uint_size * self.capacity
        align = self.pair_type_size
        len_rounded_up = (((((hashes + align) % self.modulo - 1) % self.modulo) & ~(
                (align - 1) % self.modulo)) % self.modulo - hashes) % self.modulo

        pairs_offset = hashes + len_rounded_up
        pairs_start = gdb.Value(start + pairs_offset).cast(self.pair_type.pointer())

        for index in range(self.size):
            table_index = self.valid_indices[index]
            idx = table_index & self.capacity_mask
            element = (pairs_start + idx).dereference()
            if self.show_values:
                yield (f"key{index}", element[ZERO_FIELD])
                yield (f"val{index}", element[FIRST_FIELD])
            else:
                yield (f"[{index}]", element[ZERO_FIELD])

    def display_hint(self):
        return "map" if self.show_values else "array"


class StdHashMapProvider:
    def __init__(self, valobj, show_values=True):
        self.valobj = valobj
        self.show_values = show_values

        table = self.table()
        capacity = int(table["bucket_mask"]) + 1
        ctrl = table["ctrl"]["pointer"]

        self.size = int(table["items"])
        self.pair_type = table.type.template_argument(0).strip_typedefs()

        self.new_layout = not table.type.has_key("data")
        if self.new_layout:
            self.data_ptr = ctrl.cast(self.pair_type.pointer())
        else:
            self.data_ptr = table["data"]["pointer"]

        self.valid_indices = []
        for idx in range(capacity):
            address = ctrl + idx
            value = address.dereference()
            is_presented = value & 128 == 0
            if is_presented:
                self.valid_indices.append(idx)

    def table(self):
        if self.show_values:
            hashbrown_hashmap = self.valobj["base"]
        elif self.valobj.type.fields()[0].name == "map":
            # BACKCOMPAT: rust 1.47
            # HashSet wraps std::collections::HashMap, which wraps hashbrown::HashMap
            hashbrown_hashmap = self.valobj["map"]["base"]
        else:
            # HashSet wraps hashbrown::HashSet, which wraps hashbrown::HashMap
            hashbrown_hashmap = self.valobj["base"]["map"]
        return hashbrown_hashmap["table"]

    def to_string(self):
        if self.show_values:
            return f"HashMap(size={self.size})"
        else:
            return f"HashSet(size={self.size})"

    def children(self):
        pairs_start = self.data_ptr

        for index in range(self.size):
            idx = self.valid_indices[index]
            if self.new_layout:
                idx = -(idx + 1)
            element = (pairs_start + idx).dereference()
            if self.show_values:
                yield (f"key{index}", element[ZERO_FIELD])
                yield (f"val{index}", element[FIRST_FIELD])
            else:
                yield (f"[{index}]", element[ZERO_FIELD])

    def display_hint(self):
        return "map" if self.show_values else "array"
