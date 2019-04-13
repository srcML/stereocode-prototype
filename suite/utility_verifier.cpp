class suiteOfTests : public CppUnit::TestFixture {
    /* snip */
public:
    void ageTest(){
        int age = ClassImTesting.getAge();

        // exception asserts:
        CPPUNIT_ASSERT_THROW( ClassImTesting->testAge(age - 1), WrongAgeException);
        CPPUNIT_ASSERT_NO_THROW(  ClassImTesting->testAge(age), WrongAgeException);

        // inverse asserts:
        if(age != 18)
            CPPUNIT_FAIL("Must be 18");
        CPPUNIT_ASSERT_ASSERTION_FAIL( CPP_UNIT_ASSERT( age != 18 ));
    }

void test_method()
{
    try {
        // at1 is a class member, so it can be used in a method. Assume other code initialized at1...
        CPPUNIT_ASSERT( at1->name() == "AttrTable" );

        // It's common to call CPPUNIT_ASSERT() more than once
        CPPUNIT_ASSERT( at1->size() == 7 );
    }
    catch( Error &e ) {
        // CppUnit does not know about exceptions other than its own, so if the code under test throws,
        // it can lead to some odd messages. Catching the exceptions and then using CPPUNIT_FAIL is a 
        // good approach to that issue.
        CPPUNIT_FAIL( "AttrTable threw an exception: " + e.get_error_message() )
    }
}
    
};
