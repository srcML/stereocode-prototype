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
	for(int i=0; i<10; ++i{
        	if(age != 18){
            		CPPUNIT_FAIL("Must be 18");
        		CPPUNIT_ASSERT_ASSERTION_FAIL( CPP_UNIT_ASSERT( age != 18 ));
		}
	}
    }
};
