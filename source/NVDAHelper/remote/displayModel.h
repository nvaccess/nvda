#ifndef NVDAHELPER_REMOTE_DISPLAYMODEL_H
#define NVDAHELPER_REMOTE_DISPLAYMODEL_H

#include <map>
#include <deque>
#include <windows.h>

struct displayModelChunk_t{
	RECT rect;
	std::wstring text;
	std::deque<int> characterXArray;
/**
 * Truncates the chunk's text so that only the text that fits in the resulting rectangle is left.  
 * @param truncatePointX the x position at which to truncate
 * @param truncateBefore if true then the chunk is truncated from the left all the way up to  truncation point, if false then its truncated from the point to the end.
 */
	void truncate(int truncatePointX, BOOL truncateBefore);
};

typedef std::map<std::pair<int,int>,displayModelChunk_t*> displayModelChunksByPointMap_t;

/**
 * Holds rectanglular chunks of text, and allows inserting chunks, clearing rectangles, and rendering text in a given rectangle.
 */
class displayModel_t {
	private:
	volatile long _refCount; //Internal ref count
	displayModelChunksByPointMap_t _chunksByXY; //indexes the chunks by x,y
	displayModelChunksByPointMap_t _chunksByYX; //indexes the chunks by y,y

	protected:

/**
 * Overloaded insertChunk to take an already made chunk
 * @param chunk an already made chunk
 */
	void insertChunk(displayModelChunk_t* chunk);

	public:

/**
 * constructor
 */
	displayModel_t();

/**
 * destructor
 */
	~displayModel_t();

/**
 * Increments the reference count by 1.
 * @return the new reference count.
 */
	long AddRef();

/**
 * Decrements the reference count by 1, and if it hits 0, deletes itself.
 * @return the new ref count.
 */
	long Release();

/**
 * Finds out how many chunks this model contains.
 */
	int getChunkCount();

/**
 * Inserts a text chunk in to the model.
 * @param rect the rectangle bounding the text.
 * @param text the string of unicode text in the chunk.
 * @param characterEndXArray an array of x positions for the end of each character.
 */
	void insertChunk(const RECT& rect, const std::wstring& text, int* characterEndXArray);

/**
 * Removes all chunks intersecting the given rectangle. Currently this must be called before inserting chunks as chunks should never overlap.
 * @param rect the rectangle to clear.
 */
	void clearRectangle(const RECT& rect);

/**
 * Copies the chunks intersecting the given rectangle, in to the given display model, starting from the given coordinates.
 * @param rect the rectangle intersecting all the chunks in this model that will be copied.
 * @param otherModel a pointer to the displayModel the chunks should be copied to (if NULL then this model is used) 
 * @param otherX the x coordinate in the destination model where the rectangle's left edge  starts
 * @param otherY the y coordinate in the destnation model where the rectangle's top edge starts
 */
	void copyRectangleToOtherModel(RECT& rect,displayModel_t* otherModel, int otherX, int otherY);

/**
 * Fetches the text contained in all chunks intersecting the given rectangle if provided, otherwize the text from all chunks in the model.
 * The chunks are ordered by Y and then by x.
 * @param rect the retangle which intersects the wanted chunks.
 * @param text a string in which all the rendered text will be placed.
 */
	void renderText(const RECT* rect, std::wstring& text);

};

#endif
