"""
Module holding main crawler for __slots__ based objects
"""

import logging
from typing import Union

from objectcrawler.entity import Entity


logger = logging.getLogger(__name__)


class Crawler:
    """
    Takes an object `obj`, and attempts to recursively crawl the __slots__
    """

    __slots__ = ["obj", "indent", "continuation", "data"]

    def __init__(self, obj):
        self.obj = obj
        self.data = []

        self._crawl(obj, initialise=True)

    def __str__(self):
        return self.tree()

    def __sub__(self, other):
        diff = []
        for item in self.data:
            if item not in other.data:
                item.diff = True
            diff.append(item)

        diff.append(None)
        for item in other.data:
            if item not in self.data:
                item.diff = True
            diff.append(item)

        return self.tree(diff)

    def tree(
        self,
        data: Union[None, list] = None,
        debug: bool = False,
        whitespace: int = 2,
        branch_len: int = 1,
    ) -> str:
        """
        Analyse the stored object

        Args:
            data:
                explicitly set data list (for differences)
            debug:
                prints extra debug info if True
            whitespace:
                Sets level of whitespace at the end of each column
            branch_len:
                Sets length of "branch" horizontal lines
        """
        # pylint: disable=too-many-locals, used-before-assignment
        # pylint: disable=too-many-branches, too-many-statements
        logger.info("generating tree")
        if data is None:
            logger.debug("no data provided, generating tree")
            self._crawl(self.obj, initialise=True)

            data = self.data

        # calculate column widths, pre-fill with title lengths
        widths = {"assignment": 10, "value": 5, "classname": 9, "source": 6}
        if debug:
            widths.update({"entity": 6, "parent": 6, "nchildren": 8})

        # cache a list of lines, for later treating dependent on col widths
        cache = []
        indents = {}
        indents_used = {}
        for item in data:
            if item is None:
                cache.append([None] * len(widths))
                continue
            logger.debug("treating item %s", item)
            logger.debug("parent is %s", item.parent)
            if item.parent not in indents:
                indent = 0
                logger.debug("\t\tparent %s not in indents, setting to 0", item.parent)
            else:
                indent = indents[item.parent] + 1
                logger.debug("\t\tfound parent %s at indent {indent - 1}", item.parent)

            indents[item] = indent
            logging.debug("\tindent level set to %s", indent)

            branch = "─" * branch_len + " "
            if indent == 0:
                indentstr = ""
            else:
                # generate basic indent string, taking branch length into account
                indentstr = ("│" + " " * (branch_len + 1)) * (indent - 1)
                try:
                    indents_used[item.parent] += 1
                except KeyError:
                    indents_used[item.parent] = 1
                logger.debug(
                    "\titem %s has used %s indents of max %s",
                    item,
                    indents_used[item.parent],
                    item.parent.nchildren
                )
                if indents_used[item.parent] >= item.parent.nchildren:
                    indentstr += "└" + branch
                else:
                    indentstr += "├" + branch

            line = []
            for k in widths:  # pylint: disable=consider-using-dict-items
                if k == "value" and item.iterable and item.iterable > 0:
                    line.append(f"iterable: {item.classname}")
                    continue
                if k == "entity":
                    val = str(item)
                else:
                    val = str(getattr(item, k))

                if item.diff and k in ("assignment", "value"):
                    val = f"\x1b[31m{val}\x1b[0m"

                if k == "assignment":
                    val = indentstr + val

                line.append(val)
                # update the lengths if necessary
                if len(val) > widths[k]:
                    widths[k] = len(val)
            # add this line
            cache.append(line)

        # generate the true output
        # start with the header
        header = []
        spacer = []
        for col, width in widths.items():
            header.append(col.ljust(width + whitespace))
            spacer.append("─" * (width + whitespace))
        uspacer = "┬─".join(spacer)
        spacer = "┼─".join(spacer)
        header = "│ ".join(header)

        # now generate table
        output = [uspacer, header, spacer]
        for line in cache:
            tmp = []
            spacer = False
            for idx, item in enumerate(line):
                width = list(widths.values())[idx]
                ljust = width + whitespace

                if item is None:
                    tmp.append("─" * ljust)
                    spacer = True
                    continue

                # need to adjust for colouration, if present
                if "\x1b[31m" in item:
                    ljust += 9
                tmp.append(item.ljust(ljust))

            if not spacer:
                output.append("│ ".join(tmp))
            else:
                output.append("┼─".join(tmp))

        return "\n".join(output)

    def _crawl(
        self,
        obj,
        assignment: str = "~",
        source: Union[None, str] = None,
        parent: Union[None, Entity] = None,
        initialise: bool = True,
    ) -> Entity:
        """
        Recursively crawl `obj`

        Args:
            obj:
                object in question
            assignment:
                explicitly set the variable to which obj is assigned.
                Entity tries to retrieve it otherwise
            source:
                explicitly set the source (for recursion)
            parent:
                set the parent (for recursion)
            initialise:
                wipes the data tree for a fresh run if True
        """
        # pylint: disable=too-many-arguments, too-many-branches
        logger.debug("crawling object %s", obj)
        obj_entity = Entity(obj, assignment=assignment, source=source, parent=parent)
        if initialise:
            self.data = [obj_entity]
        elif obj_entity not in self.data:
            self.data.append(obj_entity)

        for o in obj.__class__.__mro__:
            logger.debug("parsing mro object %s", o)
            source = o.__name__
            if source == "object":
                continue

            members = getattr(o, "__slots__", [])

            if hasattr(obj, "__dict__"):
                for item in obj.__dict__:
                    if not item.startswith("__"):
                        logger.debug("\tadding %s", item)
                        members.append(item)
                    else:
                        logger.debug("\tskipped %s", item)

            if len(members) == 0:
                continue

            obj_entity.nchildren += len(members)

            for item in members:
                try:
                    tmp = getattr(obj, item)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    tmp = str(e)

                parent = self._crawl(
                    tmp,
                    assignment=item,
                    source=source,
                    parent=obj_entity,
                    initialise=False,
                )
                # if we have an iterable, we should iterate over it and expand the objects
                if not isinstance(tmp, str) and hasattr(tmp, "__iter__"):
                    parent.nchildren += len(tmp)
                    try:
                        for k, v in tmp.items():
                            self._crawl(
                                v,
                                assignment=str(k),
                                source=source,
                                parent=parent,
                                initialise=False,
                            )
                    except AttributeError:
                        for i, v in enumerate(tmp):
                            self._crawl(
                                v,
                                assignment=str(i),
                                source=source,
                                parent=parent,
                                initialise=False,
                            )
        # return the object for further iteration if needed within recursion
        return obj_entity

    @property
    def str(self) -> str:
        """
        Return result as a string.

        This will initiate a crawl

        :return:
            (str) result
        """
        return str(self)

    def print(self, *args, **kwargs) -> None:
        """
        Print self

        This will initiate a crawl

        See `Tree` for args

        :return:
            None
        """
        print(self.tree(*args, **kwargs))
