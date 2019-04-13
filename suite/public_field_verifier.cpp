/* -*- Mode: C++; tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 4 -*- */
/*
 * This file is part of the LibreOffice project.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

#include <com/sun/star/frame/Desktop.hpp>

#include <comphelper/processfactory.hxx>
#include <sfx2/app.hxx>
#include <sfx2/objsh.hxx>
#include <sfx2/sfxbasemodel.hxx>
#include <test/unoapi_test.hxx>
#include <vcl/bitmapaccess.hxx>
#include <vcl/pngwrite.hxx>
#include <vcl/gdimtf.hxx>
#include <tools/stream.hxx>

using namespace com::sun::star;

class Test : public UnoApiTest
{

protected:
		void uint32ConstructorTest(void);
		void floatConstructorTest(void);
		void copyConstructorTest(void);
		void assignmentOperatorTest(void);
		void floatValueTest(void);
		void stringValueTest(void);
		void encodedValueTest(void);

	private:
		Test* test1;
		Test* test2;
		Test* test3;
		Test* test4;
		Test* test5;
		Test* test6;
		Test* test7;
		Test* test8;
		Test* test9;
		Test* test10;
		Test* test11;
public:

    Bitmap load(const char* pName)
    {
        OUString aFileURL;
        createFileURL(OUString::createFromAscii(pName), aFileURL);
        mxComponent = loadFromDesktop(aFileURL, "com.sun.star.drawing.DrawingDocument");
        SfxBaseModel* pModel = dynamic_cast<SfxBaseModel*>(mxComponent.get());
        CPPUNIT_ASSERT(pModel);
        SfxObjectShell* pShell = pModel->GetObjectShell();
        std::shared_ptr<GDIMetaFile> xMetaFile = pShell->GetPreviewMetaFile();
        BitmapEx aResultBitmap;
        CPPUNIT_ASSERT(xMetaFile->CreateThumbnail(aResultBitmap));
        // If this is set, the metafile will be dumped as a PNG one for debug purposes.
        char* pEnv = getenv("CPPCANVAS_DEBUG_EMFPLUS_DUMP_TO");
    // The green star was missing.
    Color aColor(pAccess->GetPixel(142, 140).GetColor());
    CPPUNIT_ASSERT_EQUAL(sal_uInt8(0), aColor.GetRed());
    CPPUNIT_ASSERT_EQUAL(sal_uInt8(0), aColor.GetBlue());
    CPPUNIT_ASSERT(aColor.GetGreen() == 0xfe || aColor.GetGreen() == 0xff);

        return aResultBitmap.GetBitmap();
    }
    

void assignmentOperatorTest(void)
{
   FixedPoint special1(*test7);
   special1 = *test1;
   CPPUNIT_ASSERT_EQUAL(false, special1.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(1), special1.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special1.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special2(*test7);
   special2 = *test2;
   CPPUNIT_ASSERT_EQUAL(true, special2.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(1), special2.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special2.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special3(*test7);
   special3 = *test3;
   CPPUNIT_ASSERT_EQUAL(false, special3.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(2), special3.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special3.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special4(*test7);
   special4 = *test4;
   CPPUNIT_ASSERT_EQUAL(true, special4.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(2), special4.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.5, special4.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special5(*test7);
   special5 = *test5;
   CPPUNIT_ASSERT_EQUAL(false, special5.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(3), special5.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.14, special5.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special6(*test7);
   special6 = *test6;
   CPPUNIT_ASSERT_EQUAL(false, special6.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(100), special6.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99, special6.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special7(*test6);   // using 6 to test 7
   special7 = *test7;
   CPPUNIT_ASSERT_EQUAL(false, special7.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(0), special7.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special7.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special8(*test7);
   special8 = *test8;
   CPPUNIT_ASSERT_EQUAL(true, special8.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special8.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99997, special8.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special9(*test7);
   special9 = *test9;
   CPPUNIT_ASSERT_EQUAL(false, special9.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special9.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99997, special9.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special10(*test7);
   special10 = *test10;
   CPPUNIT_ASSERT_EQUAL(false, special10.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special10.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99994, special10.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint special11(*test10);
   special11 = special11;
   CPPUNIT_ASSERT_EQUAL(false, special11.fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special11.fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99994, special11.fFractPart, FixedPoint::kMarginOfError());

   FixedPoint* special12;
   special12 = test10;
   *special12 = *test10;
   CPPUNIT_ASSERT_EQUAL(false, special12->fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special12->fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99994, special12->fFractPart, FixedPoint::kMarginOfError());

   FixedPoint* special13;
   special13 = test10;
   *special13 = *test10 = *test6;
   CPPUNIT_ASSERT_EQUAL(false, test10->fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(100), test10->fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99, test10->fFractPart, FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_EQUAL(false, special13->fNegative);
   CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(100), special13->fIntPart);
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99, special13->fFractPart, FixedPoint::kMarginOfError());
}
    uno::Reference<lang::XComponent> mxComponent;
};


