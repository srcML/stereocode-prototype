
string::size_type
NTupleController::
findWhite ( const std::string & line, unsigned int left, bool tabs_only )
{
	string::size_type right = line.find( '\t', left );

	if( line.find( '\n', left ) < right ) right = line.find( '\n', left );

	if ( tabs_only == false ) { 
		if( line.find( ' ', left ) < right ) right = line.find( ' ', left );
	}

	return right;
}

string::size_type
NTupleController::
findWhite ( const std::string& line, unsigned int left, bool tabs_only )
{
	string::size_type right = line.find( '\t', left );

	if( line.find( '\n', left ) < right ) right = line.find( '\n', left );

	if ( tabs_only == false ) { 
		if( line.find( ' ', left ) < right ) right = line.find( ' ', left );
	}

	return right;
}
