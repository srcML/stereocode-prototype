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

void testEquality()
  {
    CPPUNIT_ASSERT(1 == 1);
  }

  void testCreation()
  {
    MyClass<callable>* tp = new MyClass<callable>(1);
    CPPUNIT_ASSERT_MESSAGE(tp->done() == true);
    delete tp;
  }

void example ()
    {
    	CPPUNIT_ASSERT (1 == 1);
    }



    void anotherExample ()
    {
    	CPPUNIT_ASSERT (2 == 2);
    }

};
