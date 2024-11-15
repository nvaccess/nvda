/*
This file is a part of the NVDA project.
URL: http://www.nvda-project.org/
Copyright 2006-2023 NVDA contributors.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 2.0, as published by
    the Free Software Foundation.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
This license can be found at:
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

#ifndef VIRTUALBUFFER_BACKENDS_EXAMPLE_H
#define VIRTUALBUFFER_BACKENDS_EXAMPLE_H

#include <vbufBase/backend.h>
#include <optional>

class LabelInfo;

class GeckoVBufBackend_t: public VBufBackend_t {
	private:

	VBufStorage_fieldNode_t* fillVBuf(
		IAccessible2* pacc,
		VBufStorage_buffer_t* buffer,
		VBufStorage_controlFieldNode_t* parentNode,
		VBufStorage_fieldNode_t* previousNode,
		IAccessibleTable2* paccTable2=NULL,
		long tableID=0, const wchar_t* parentPresentationalRowNumber=NULL,
		bool ignoreInteractiveUnlabelledGraphics=false
	);

	/* Fill the virtual buffer with information required for aria details (annotations) information.
	 * @note: Expected to be called by fillVBuf
	 * @param docHandle: The handle of the current document, required to identify target/origin of an annotation relationship.
	 * @param pacc: The IAccessible for the nodeBeingFilled
	 * @param buffer: The virtual buffer that is being filled, used to get the other side of the relationship (target/origin)
	 * @param nodeBeingFilled: The current node being filled. This maybe a target, origin, or neither.
	 * @param nodeBeingFilledRole: The role of the parentNode, used to set the detailsRole in the origin of the annotation relationship.
	 */
	void fillVBufAriaDetails(
		int docHandle,
		CComPtr<IAccessible2> pacc,
		VBufStorage_buffer_t& buffer,
		VBufStorage_controlFieldNode_t& nodeBeingFilled,
		const std::wstring& nodeBeingFilledRole
	);

	/* Fill the virtual buffer with information required to support aria-errormessage.
	 *
	 * @param pacc: The IAccessible for the node being filled.
	 * @param nodeBeingFilled: The current node being filled. This will be the origin of an error relation.
	 * @result: If `pacc` is the origin of an error relation, `nodeBeingFilled` will gain an attribute `errorMessage` with the text of the target end of the relation.
	 */
	void fillVBufAriaError(
		CComPtr<IAccessible2> pacc,
		VBufStorage_controlFieldNode_t& nodeBeingFilled
	);

	void versionSpecificInit(IAccessible2* pacc);

	void fillTableCellInfo_IATable2(VBufStorage_controlFieldNode_t* node, IAccessibleTableCell* paccTableCell);

	std::wstring toolkitName;

	/* Get the IAccessible IDs for all relation targets of the specified relation type.
	* @param ia2TargetRelation: The type of relation to fetch. Use IA2_RELATION_* constants
			from 'include/ia2/api/AccessibleRelation.idl' becomes 'build/<arch>/ia2.h'
	* @param pacc2: The element to fetch relations for.
	*/
	std::vector<int> getAllRelationIdsForRelationType(LPCOLESTR ia2TargetRelation, IAccessible2* pacc2);

	/*
	*/
	std::optional< LabelInfo > getLabelInfo(IAccessible2* pacc2);

	/* Get relation elements of the type.
	 * @param ia2TargetRelation: The type of relation to fetch. Use IA2_RELATION_* constants
			from 'include/ia2/api/AccessibleRelation.idl' becomes 'build/<arch>/ia2.h'
	 * @param element: The element to fetch relations for.
	 * @param numRelations: If supplied, only return up to numRelations. Note: Fetches all by default.
	 */
	std::vector<CComQIPtr<IAccessible2>> getRelationElementsOfType(
		LPCOLESTR ia2TargetRelation,
		IAccessible2_2* element,
		const std::optional<std::size_t> numRelations = {}
	);
	CComPtr<IAccessible2> getSelectedItem(IAccessible2* container,
		const std::map<std::wstring, std::wstring>& attribs);

	bool isRootDocAlive();

	CComPtr<IAccessible2> rootDocAcc;

	protected:

	static void CALLBACK renderThread_winEventProcHook(HWINEVENTHOOK hookID, DWORD eventID, HWND hwnd, long objectID, long childID, DWORD threadID, DWORD time);

	virtual void renderThread_initialize();

	virtual void renderThread_terminate();

	virtual void render(VBufStorage_buffer_t* buffer, int docHandle, int ID, VBufStorage_controlFieldNode_t* oldNode=NULL);

	virtual ~GeckoVBufBackend_t();

	public:

	GeckoVBufBackend_t(int docHandle, int ID);

};

#endif
