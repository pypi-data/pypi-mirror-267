#
#    Module `diskinfo`: implements class `DiskInfo`.
#    Peter Sulyok (C) 2022-2024.
#
import os
from typing import List
from diskinfo.disktype import DiskType
from diskinfo.disk import Disk


class DiskInfo:
    """This class implements disk exploration functionality. At class initialization time all existing disks
    will be explored automatically (empty loop devices will be skipped). In a next step,
    :meth:`~diskinfo.DiskInfo.get_disk_number()` method can return the number of identified disk and
    :meth:`~diskinfo.DiskInfo.get_disk_list()` method can return the list of the identified disks.
    In both cases disk type filters can be applied to get only a subset of the discovered disks. The filters are
    set of :class:`~diskinfo.DiskType` values.

    Operator ``in`` is also implemented for this class. Caller can check if a :class:`~diskinfo.Disk` class instance
    can be found on the list of the identified disks.

    Example:
        A code example about the basic use of the class and the use of the ``in`` operator.

            >>> from diskinfo import Disk, DiskType, DiskInfo
            >>> di = DiskInfo()
            >>> n = di.get_disk_number(included={DiskType.SSD}, excluded={DiskType.HDD})
            >>> print(f"Number of SSDs: {n}")
            Number of SSDs: 3
            >>> d = Disk("sda")
            >>> print(d in di)
            True
        """

    __disk_list: List[Disk]           # List of discovered disks.

    def __init__(self):
        """See class definition."""

        # Initialize class variables.
        self.__disk_list = []

        # Iterate on list of block devices.
        for file_name in os.listdir('/sys/block'):
            new_disk = Disk(disk_name=file_name)
            # Empty loop devices are skipped
            if not (new_disk.is_loop() and new_disk.get_size() == 0):
                self.__disk_list.append(new_disk)

    def get_disk_number(self, included: set = None, excluded: set = None) -> int:
        """Returns the number of the disks. The caller can specify inclusive and exclusive filters for disk types.
        If no filters are specified then the default behavior is to include all disk types and to exclude nothing.

        Args:
            included (set): filter set for included disk types
            excluded (set): filter set for excluded disk types

        Returns:
            int: number of the (filtered) disks

        Raises:
            ValueError: if the same disk type is on both included and excluded filter sets

        Example:
            A code example about using filters: it counts the number of SSDs excluding NVME disks.

            >>> from diskinfo import DiskType, DiskInfo
            >>> di = DiskInfo()
            >>> n = di.get_disk_number(included={DiskType.SSD}, excluded={DiskType.HDD})
            >>> print(f"Number of SSDs: {n}")
            Number of SSDs: 3
        """
        disk_number: int    # Number of disk counted

        # Set the default filter if not specified.
        if not included:
            included = {DiskType.HDD, DiskType.SSD, DiskType.NVME, DiskType.LOOP}
        if not excluded:
            excluded = set()

        # Check invalid filters.
        if included.intersection(excluded):
            raise ValueError("Parameter error: same value on included and excluded list.")

        # Count number of disks based on the specified filters.
        disk_number = 0
        for disk in self.__disk_list:
            disk_type = disk.get_type()
            if disk_type in included and disk_type not in excluded:
                disk_number += 1

        return disk_number

    def get_disk_list(self, included: set = None, excluded: set = None, sorting: bool = False,
                      rev_order: bool = False) -> List[Disk]:
        """Returns the list of identified disks. The caller can specify inclusive and exclusive filters for disk types.
        If no filters are specified the default behavior is to include all disk types and to exclude nothing.
        The list can be sorted based on the disk `name` in alphabetical order. Caller can also request sorting
        in reverse order.

        Args:
            included (set): filter set for included disk types
            excluded (set): filter set for excluded disk types
            sorting (bool): disk list will be sorted based on `name` string
            rev_order (bool): sorting in reverse order

        Returns:
            List[Disk]: list of the (filtered) disks

        Raises:
            ValueError: if the same disk type is on both included and excluded filter sets

        Example:
            A code example about using filters and sorting: it will list the device path of the sorted list
            of the HDDs:

            >>> from diskinfo import DiskType, DiskInfo
            >>> di = DiskInfo()
            >>> disks = di.get_disk_list(included={DiskType.HDD}, sorting=True)
            >>> for d in disks:
            ...     print(d.get_path())
            ...
            /dev/sda
            /dev/sdb
            /dev/sdc
        """
        result: List[Disk] = []

        # Set default filters if not specified.
        if not included:
            included = {DiskType.HDD, DiskType.SSD, DiskType.NVME, DiskType.LOOP}
        if not excluded:
            excluded = set()

        # Check invalid filters.
        if included.intersection(excluded):
            raise ValueError("Parameter error: same value on included and excluded list.")

        # Collect selected disks based on the specified filters.
        for disk in self.__disk_list:
            disk_type = disk.get_type()
            if disk_type in included and disk_type not in excluded:
                result.append(disk)

        # Sort the result list if needed.
        if sorting:
            result.sort(reverse=rev_order)

        return result

    def __contains__(self, item):
        """Returns True if a specified disk is in the discovered list of disk otherwise False."""

        # Check identified list of disks if the specified disk can be found.
        for disk in self.__disk_list:
            if item.get_serial_number() == disk.get_serial_number():
                return True
        return False

    def __repr__(self):
        """String representation of the DiskInfo class."""
        return f"DiskInfo(number_of_disks={len(self.__disk_list)}, " \
               f"list_of_disks={self.__disk_list})"

# End
