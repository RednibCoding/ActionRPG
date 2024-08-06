from typing import List, Dict, Tuple, Any
import cave

class Client():
	def __init__(self, addr: str = "localhost", port: int = 33333): ... 
	def isConnected(self) -> bool: ... 
	def update(self) -> None: ... 
	def send(self, pkg: network.Package, reliable: bool = True) -> None: ... 
	def popPackages(self) -> List[network.Package]: ... 



def init() -> None: ... 
def shutdown() -> None: ... 
def isInitialized() -> bool: ... 

class PackageException():
	msg: str 
	def __init__(self, _msg: str): ... 
	def what(self) -> str: ... 


class Package():

	# Enum: networkPackagePackageMode:# "Package" class Enumeration.
	READ : int 
	WRITE : int 


	# Enum: networkPackageDataType:# "Package" class Enumeration.
	TYPE_INVALID : int 
	TYPE_INT : int 
	TYPE_LONG_INT : int 
	TYPE_FLOAT : int 
	TYPE_BOOL : int 
	TYPE_VEC3 : int 
	TYPE_STRING : int 

	def __init__(self, readMode: bool = False): ... 
	def __init__(self, data: None, len: int): ... 
	def __init__(self, other: network.Package): ... 
	def writeInt(self, value: int) -> None: ... 
	def writeLongInt(self, value: int) -> None: ... 
	def writeFloat(self, value: float) -> None: ... 
	def writeBool(self, value: bool) -> None: ... 
	def writeVector3(self, value: cave.Vector3) -> None: ... 
	def writeString(self, value: str) -> None: ... 
	def readInt(self) -> int: ... 
	def readLongInt(self) -> int: ... 
	def readFloat(self) -> float: ... 
	def readBool(self) -> bool: ... 
	def readVector3(self) -> cave.Vector3: ... 
	def readString(self) -> str: ... 
	def getNextDataType(self) -> network.Package.DataType: ... 
	def getBufferSize(self) -> int: ... 


class ServerPeer():
	def __init__(self, peer: ENetPeer): ... 
	def send(self, pkg: network.Package, reliable: bool = True) -> None: ... 


class ServerPackage():
	sender: network.ServerPeer 
	package: network.Package 


class Server():
	def __init__(self, addr: .str = "localhost", port: int = 33333): ... 
	def update(self) -> None: ... 
	def sendToAll(self, pkg: network.Package, reliable: bool = True) -> None: ... 
	def popPackages(self) -> List[network.ServerPackage]: ... 
	def getNumClients(self) -> int: ... 

