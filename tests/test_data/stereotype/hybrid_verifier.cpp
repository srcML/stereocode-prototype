// CppUnit-Tutorial
// file: fractiontest.cc
#include "fractiontest.h"
#include "pch.h"

CPPUNIT_TEST_SUITE_REGISTRATION(fractiontest);

class fractiontest : public CppUnit::TestFixture  {
	double			m_value1;
    	double			m_value2;
void equalTest(void)
{
	// test successful, if true is returned
	CPPUNIT_ASSERT(*d == *e);
	CPPUNIT_ASSERT(Fraction(1) == Fraction(2, 2));
	CPPUNIT_ASSERT(Fraction(1) != Fraction(1, 2));
	// both must have equal valued
	CPPUNIT_ASSERT_EQUAL(*f, *g);
	CPPUNIT_ASSERT_EQUAL(*h, Fraction(0));
	CPPUNIT_ASSERT_EQUAL(*h, Fraction(0, 1));
}

void testEquals ()
    {
        std::auto_ptr<long>	l1 (new long (12));
        std::auto_ptr<long>	l2 (new long (12));


    	CPPUNIT_ASSERT_DOUBLES_EQUAL (m_value1, 2.0, 0.01);
    	CPPUNIT_ASSERT_DOUBLES_EQUAL (m_value2, 3.0, 0.01);
    	CPPUNIT_ASSERT_EQUAL (12, 12);
    	CPPUNIT_ASSERT_EQUAL (12L, 12L);
    	CPPUNIT_ASSERT_EQUAL (*l1, *l2);


    	CPPUNIT_ASSERT(12L == 12L);
    	CPPUNIT_ASSERT_DOUBLES_EQUAL (12.0, 11.99, 0.5);
    }
};
