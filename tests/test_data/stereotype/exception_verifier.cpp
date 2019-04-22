// CppUnit-Tutorial
// file: fractiontest.cc
#include "fractiontest.h"
#include "pch.h"

CPPUNIT_TEST_SUITE_REGISTRATION(fractiontest);

class fractiontest : public CppUnit::TestFixture  {

void exceptionTest(void)
{
	// an exception has to be thrown here
	CPPUNIT_ASSERT_THROW(Fraction(1, 0), DivisionByZeroException);
}


};
