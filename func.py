#  Philsoft  (c) 2021.

from typing import Dict


def removeFileSelectFromDict(data: Dict):

	"""
	:param data:
	:type dict:
	:return data:
	:rtype dict:
	"""

	del data['FILE_IMG']
	del data['FILE_DOK']
	del data['FILE_SCH']
	del data['FILE_BRD']
	del data['FILE_STP']
	return data
