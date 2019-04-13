class ComplexNumberTest : public CppUnit::TestFixture  {
private:
  Complex *m_10_1, *m_1_1, *m_11_2;
public:

  void tearDown() 
  {
    delete m_10_1;
    delete m_1_1;
    delete m_11_2;
  }

  
  //more testing
  void testAddition()
  {
    CPPUNIT_ASSERT( *m_10_1 + *m_1_1 == *m_11_2 );
  }
};
