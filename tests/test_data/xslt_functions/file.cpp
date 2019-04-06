int      compareItems( QCollection::Item s1, QCollection::Item s2 )
{ return qstricmp((const char*)s1,
		  (const char*)s2); }


/** @stereotype collaborator pure_stateless */
inline QString &QString::append( QChar c )
{ return operator+=(c); }


/** @stereotype collaborational-command collaborator pure_stateless */
QDataStream& QGDict::read( QDataStream &s, QCollection::Item &item )
{
  item = 0;
  return s;
}

/** @stereotype collaborational-command collaborator pure_stateless */
int QGVector::compareItems( Item d1, Item d2 )
{
  return d1 != d2;                // compare pointers
}

/** @stereotype collaborator pure_stateless */
QCollection::Item QCollection::newItem( Item d )
{
  return d;                    // just return reference
}

/** @stereotype property collaborator pure_stateless */
QString QFileInfo::readLink() const
{
  QString r;
  return r;
}

/** @stereotype collaborator pure_stateless */
void    setPattern( const QString& pattern )
{ operator=( pattern ); } 
