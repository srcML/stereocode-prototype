// DiskDataTest.cpp: implementation of the DiskDataTest class.
//
//////////////////////////////////////////////////////////////////////

#include "stdafx.h"
#include "DiskDataTestCase.h"

#ifdef _DEBUG
#undef THIS_FILE
static char THIS_FILE[]=__FILE__;
#define new DEBUG_NEW
#endif


//
// These are correct values stored in auxiliar file
//
#define AUX_FILENAME	"..\\Test\\ok_data.dat"
#define FILE_NUMBER		19
#define FILE_STRING		"this is correct text stored in auxiliar file"



//
// Aux function:
//		Read all file and allocates a buffer 
void DiskDataTestCase::storeTest()
{
	DATA	d;
	DWORD  	tmpSize, auxSize;
	BYTE 	*tmpBuff, *auxBuff;
	TCHAR	absoluteFilename[MAX_PATH];
	DWORD	size = MAX_PATH;

	// configures structure with known data
	d.number = FILE_NUMBER;
	strcpy(d.string, FILE_STRING);

	// convert from relative to absolute path

	strcpy(absoluteFilename, AUX_FILENAME);
	CPPUNIT_ASSERT( RelativeToAbsolutePath(absoluteFilename, &size) );

	// executes action
	fixture->setData(&d);
	CPPUNIT_ASSERT( fixture->store("data.tmp") );

	// Read both files contents and check results 
	tmpSize = ReadAllFileInMemory("data.tmp", tmpBuff);
	auxSize = ReadAllFileInMemory(absoluteFilename, auxBuff);


	delete [] tmpBuff;
	delete [] auxBuff;

	::DeleteFile("data.tmp");
}
