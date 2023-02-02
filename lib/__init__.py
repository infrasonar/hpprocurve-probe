import struct
import time
from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.mib.syntax_funs import SYNTAX_FUNS


def on_eventlogtime(value: bytes):
    '''
    cpqHeEventLogUpdateTime OBJECT-TYPE
    SYNTAX  OCTET STRING (SIZE (6))
    ACCESS  read-only
    STATUS  mandatory
    DESCRIPTION
        "The time stamp when the event log entry was last modified.
            field  octets  contents                  range
            =====  ======  ========                  =====
            1      1-2   year                      0..65536
            2       3    month                     1..12
            3       4    day                       1..31
            4       5    hour                      0..23
            5       6    minute                    0..59
        The year field is set with the most significant octet first.
        A value of 0 in the year indicates an unknown time stamp."
    src: CPQHLTH-MIB.mib
    '''
    # some devices seem to return 7 octets, thus we break at [:6] to strip the
    # last octect(s)
    timetuple = struct.unpack('>HBBBB', value[:6])
    ts = int(time.mktime(timetuple + (0, 0, 0, -1)))
    return ts


def on_phydrvids(value: bytes):
    '''
    cpqDaLogDrvPhyDrvIDs OBJECT-TYPE
        SYNTAX  OCTET STRING (SIZE (0..255))
        ACCESS  read-only
        STATUS  deprecated
        DESCRIPTION
            "Drive Array Logical Drive Physical Drive IDs.

            This lists the physical drive IDs which are associated with this
            logical drive. These are the same IDs which can be used as
            indices into the physical drive table. Each byte of the string
            is an index. For array controllers that support a larger number
            of drives, the Drive Array Logical Drive Extended Physical
            Drive Attachment Table should be used to determine drive
            associations."
        ::= { cpqDaLogDrvEntry 10 }
    '''
    return list(map(int, value))


SYNTAX_FUNS['hp_eventlogtime'] = on_eventlogtime
SYNTAX_FUNS['hp_phydrvids'] = on_phydrvids

# patch the syntax function because we need the raw bytes for these metrics
MIB_INDEX[MIB_INDEX['CPQHLTH-MIB']['cpqHeEventLogInitialTime']]['syntax'] = {
    'tp': 'CUSTOM', 'func': 'hp_eventlogtime',
}
MIB_INDEX[MIB_INDEX['CPQHLTH-MIB']['cpqHeEventLogUpdateTime']]['syntax'] = {
    'tp': 'CUSTOM', 'func': 'hp_eventlogtime',
}
MIB_INDEX[MIB_INDEX['CPQIDA-MIB']['cpqDaLogDrvPhyDrvIDs']]['syntax'] = {
    'tp': 'CUSTOM', 'func': 'hp_phydrvids',
}
