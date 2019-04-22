// Copyright © 2010 Scott Gustafson. All Rights Reserved.
// http://www.garlicsoftware.com

#include <cmath>
#include <iomanip>
#include <sstream>
#include <stdexcept>
#include "FixedPoint.h"
#pragma mark -
#if defined(qDebug)
#include <cppunit/extensions/HelperMacros.h>

class FixedPointTest : public CPPUNIT_NS::TestFixture {
	CPPUNIT_TEST_SUITE( FixedPointTest );
	CPPUNIT_TEST( uint32ConstructorTest );
	CPPUNIT_TEST( floatConstructorTest );
	CPPUNIT_TEST( copyConstructorTest );
	CPPUNIT_TEST( assignmentOperatorTest );
	CPPUNIT_TEST( floatValueTest );
	CPPUNIT_TEST( stringValueTest );
	CPPUNIT_TEST( encodedValueTest );
	CPPUNIT_TEST_SUITE_END();

	protected:
		void uint32ConstructorTest(void);
		void floatConstructorTest(void);
		void copyConstructorTest(void);
		void assignmentOperatorTest(void);
		void floatValueTest(void);
		void stringValueTest(void);
		void encodedValueTest(void);

	private:
		FixedPoint* test1;
		FixedPoint* test2;
		FixedPoint* test3;
		FixedPoint* test4;
		FixedPoint* test5;
		FixedPoint* test6;
		FixedPoint* test7;
		FixedPoint* test8;
		FixedPoint* test9;
		FixedPoint* test10;
		FixedPoint* test11;
};

CPPUNIT_TEST_SUITE_REGISTRATION( FixedPointTest );


void FixedPointTest::floatConstructorTest(void) {
	FixedPoint special1(1.0);
	CPPUNIT_ASSERT_EQUAL(false, special1.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(1), special1.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special1.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special2(-1.0);
	CPPUNIT_ASSERT_EQUAL(true, special2.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(1), special2.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special2.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special3(2.0);
	CPPUNIT_ASSERT_EQUAL(false, special3.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(2), special3.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special3.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special4(-2.5);
	CPPUNIT_ASSERT_EQUAL(true, special4.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(2), special4.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.5, special4.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special5(3.14);
	CPPUNIT_ASSERT_EQUAL(false, special5.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(3), special5.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.14, special5.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special6(100.99);
	CPPUNIT_ASSERT_EQUAL(false, special6.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(100), special6.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99, special6.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special7(0.0);
	CPPUNIT_ASSERT_EQUAL(false, special7.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(0), special7.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special7.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special8(-65535.99997);
	CPPUNIT_ASSERT_EQUAL(true, special8.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special8.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99997, special8.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special9(65535.99997);
	CPPUNIT_ASSERT_EQUAL(false, special9.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special9.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99997, special9.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint special10(65535.99994);
	CPPUNIT_ASSERT_EQUAL(false, special10.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(65535), special10.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.99994, special10.fFractPart, FixedPoint::kMarginOfError());

	// Note that this value is not round tripped here as -0.0 is no different from 0.0
	FixedPoint special11(-0.0);
	CPPUNIT_ASSERT_EQUAL(false, special11.fNegative);
	CPPUNIT_ASSERT_EQUAL(static_cast<UInt16>(0), special11.fIntPart);
	CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, special11.fFractPart, FixedPoint::kMarginOfError());

	FixedPoint* special100 = NULL;
	CPPUNIT_ASSERT_THROW(special100 = new FixedPoint(65535.999971), std::out_of_range);
	delete special100;

	CPPUNIT_ASSERT_THROW(special100 = new FixedPoint(-65535.999971), std::out_of_range);
	delete special100;

	CPPUNIT_ASSERT_THROW(special100 = new FixedPoint(65536.0), std::out_of_range);
	delete special100;

	CPPUNIT_ASSERT_THROW(special100 = new FixedPoint(-65536.0), std::out_of_range);
	delete special100;

	CPPUNIT_ASSERT_NO_THROW(special100 = new FixedPoint(65535.99997));
	delete special100;

	CPPUNIT_ASSERT_NO_THROW(special100 = new FixedPoint(0.999971));
	delete special100;
}



void FixedPointTest::assignmentOperatorTest(void)
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

void FixedPointTest::floatValueTest(void)
{
   CPPUNIT_ASSERT_DOUBLES_EQUAL(1.0, test1->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(-1.0, test2->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(2.0, test3->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(-2.5, test4->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(3.14, test5->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(100.99, test6->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, test7->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(FixedPoint::kMinValue(), test8->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(FixedPoint::kMaxValue(), test9->FloatValue(), FixedPoint::kMarginOfError());
   
   // ensure differentiation based on the margin of error
   CPPUNIT_ASSERT_DOUBLES_EQUAL(65535.99994, test10->FloatValue(), FixedPoint::kMarginOfError());
   CPPUNIT_ASSERT_DOUBLES_EQUAL(FixedPoint::kMaxValue() - FixedPoint::kMarginOfError(), test10->FloatValue(), 
    FixedPoint::kMarginOfError());

   CPPUNIT_ASSERT_DOUBLES_EQUAL(0.0, test11->FloatValue(), FixedPoint::kMarginOfError());
}


#endif // qDebug
