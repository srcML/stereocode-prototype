class suiteOfTests : public CppUnit::TestFixture {
    /* snip */
public:
    void ageTest(){
        int age = ClassImTesting.getAge();

        // simple asserts
        CPPUNIT_ASSERT(age == 18);
        CPPUNIT_ASSERT_MESSAGE("Must be 18", age == 18);

        // asserting equality:
        CPPUNIT_ASSERT_EQUAL(age, 18);
        CPPUNIT_ASSERT_EQUAL_MESSAGE("Must be 18", age, 18);
        CPPUNIT_ASSERT_DOUBLES_EQUAL(age * 1.0, 18.0, 1e-10);

        // exception asserts:
        CPPUNIT_ASSERT_THROW( ClassImTesting->testAge(age - 1), WrongAgeException);
        CPPUNIT_ASSERT_NO_THROW(  ClassImTesting->testAge(age), WrongAgeException);

        // inverse asserts:
        if(age != 18)
            CPPUNIT_FAIL("Must be 18");
        CPPUNIT_ASSERT_ASSERTION_FAIL( CPP_UNIT_ASSERT( age != 18 ));
    }

   void load(const char* pName)
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
        if (pEnv)
        {
            SvFileStream aStream(OUString::fromUtf8(pEnv), StreamMode::WRITE);
            vcl::PNGWriter aWriter(aResultBitmap);
            CPPUNIT_ASSERT(aWriter.Write(aStream));
        }

    // The green star was missing.
    Color aColor(pAccess->GetPixel(142, 140).GetColor());
    CPPUNIT_ASSERT_EQUAL(sal_uInt8(0), aColor.GetRed());
    CPPUNIT_ASSERT_EQUAL(sal_uInt8(0), aColor.GetBlue());
    CPPUNIT_ASSERT(aColor.GetGreen() == 0xfe || aColor.GetGreen() == 0xff);

        return aResultBitmap.GetBitmap();
    }
};
