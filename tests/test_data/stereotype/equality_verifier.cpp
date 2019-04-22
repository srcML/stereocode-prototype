#include "CartesianComplex.h"
#include "TestCartesianComplex.h"

/**
 * @author Keith Lee
 *         keithlee [ at ] unc.edu
 */

class TestCartesianComplex: public CppUnit::TestFixture  {

public:
void testAccessors( )
{
    CartesianComplex cc0_0;
    CartesianComplex cc1_0(1);
    CartesianComplex cc0_1(0, 1);
    CartesianComplex cc3_4(3, 4);
    CartesianComplex cc1_3(1, 3);
    CartesianComplex cc2_1(2, 1);

    CPPUNIT_ASSERT_EQUAL( 0.0, cc0_0.getReal() );
    CPPUNIT_ASSERT_EQUAL( 0.0, cc0_0.getImaginary() );

    CPPUNIT_ASSERT_EQUAL( 1.0, cc1_0.getReal() );
    CPPUNIT_ASSERT_EQUAL( 0.0, cc1_0.getImaginary() );

    CPPUNIT_ASSERT_EQUAL( 0.0, cc0_1.getReal() );
    CPPUNIT_ASSERT_EQUAL( 1.0, cc0_1.getImaginary() );

    CPPUNIT_ASSERT_EQUAL( 3.0, cc3_4.getReal() );
    CPPUNIT_ASSERT_EQUAL( 4.0, cc3_4.getImaginary() );

    CPPUNIT_ASSERT_EQUAL( 1.0, cc1_3.getReal() );
    CPPUNIT_ASSERT_EQUAL( 3.0, cc1_3.getImaginary() );

    CPPUNIT_ASSERT_EQUAL( 2.0, cc2_1.getReal() );
    CPPUNIT_ASSERT_EQUAL( 1.0, cc2_1.getImaginary() );
}

void testEqualityOperators( )
{
    CartesianComplex cc0_0;
    CartesianComplex cc1_0(1);
    CartesianComplex cc0_1(0, 1);

    CPPUNIT_ASSERT_EQUAL( CartesianComplex(10, 1), CartesianComplex(10, 1) );
    CPPUNIT_ASSERT( cc0_0 != cc1_0 );
    CPPUNIT_ASSERT( cc0_0 != cc0_1 );
    CPPUNIT_ASSERT( cc0_1 != cc1_0 );
}

	void testRun(){
		CPPUNIT_ASSERT_EQUAL(1.2f, greater3(1.2, 0.26, -1.2) );
		CPPUNIT_ASSERT_EQUAL(0.0f, greater3(-3.2, -1, 0) );
		CPPUNIT_ASSERT_EQUAL(3.0f, greater3(2, 3, 2) );
		CPPUNIT_ASSERT_EQUAL(5.1f, greater3(5.1, 5.1, 5.1) );
		CPPUNIT_ASSERT_EQUAL(61.02f, greater3(61.02, 61.02, 1) );
		CPPUNIT_ASSERT_EQUAL(-5.0f, greater3(-26, -10, -5) );
	}

void test_toString()
{
    CPPUNIT_ASSERT_EQUAL( std::string( "abc" ), 
			  CPPUNIT_NS::assertion_traits<const char*>::toString( "abc" ) );

    CPPUNIT_ASSERT_EQUAL( std::string( "33" ), 
			  CPPUNIT_NS::assertion_traits<int>::toString( 33 ) );

    // Test that assertion_traits<double>::toString() produces 
    // more than the standard 6 digits of precision.
    CPPUNIT_ASSERT_EQUAL( std::string( "33.1" ), 
			  CPPUNIT_NS::assertion_traits<double>::toString( 33.1 ) );
    CPPUNIT_ASSERT_EQUAL( std::string( "33.001" ), 
			  CPPUNIT_NS::assertion_traits<double>::toString( 33.001 ) );
    CPPUNIT_ASSERT_EQUAL( std::string( "33.00001" ), 
			  CPPUNIT_NS::assertion_traits<double>::toString( 33.00001 ) );
    CPPUNIT_ASSERT_EQUAL( std::string( "33.0000001" ), 
			  CPPUNIT_NS::assertion_traits<double>::toString( 33.0000001 ) );
    CPPUNIT_ASSERT_EQUAL( std::string( "33.0000000001" ), 
			  CPPUNIT_NS::assertion_traits<double>::toString( 33.0000000001 ) );
}
};
