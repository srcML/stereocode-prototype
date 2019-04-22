//collabor-command (non_dm -> a() and throw calls)

void
DataSource::
checkWidth ( const DataSource * source )
{
  unsigned int ncolumns = source -> columns ();
  if ( ncolumns != 1 ) 
       throw runtime_error ( what );
  
}

// stateless

void
DataSource::
replaceColumn ( unsigned int, 
		const std::vector < double > & array )
{
  string what ( "DataSource: The type of data source does not support "
		"replacing a column." );
  throw runtime_error ( what );
}

int
DataSource::
addColumn ( const std::string &,
	    const std::vector < double > & )
{
  string what ( "DataSource: This type of data source does not support "
		"adding a column." );
  throw runtime_error ( what );
}

// right labeling for property

double *
DataSource::
doubleArrayAt ( unsigned int row, unsigned int column ) const
{
  string what ( "DataSource: This data source is not capable of containing\n"
		"an array in a column." );
  throw runtime_error ( what );
}




void
DataSourceController::
checkWidth ( const DataSource * source, int size )
{
  ncolumns = source -> columns ();
  if ( ncolumns != size ) {
    string what ( "DataSource: Number of columns of source (" );
    what += String::convert ( ncolumns );
    what += ") not equal to current (";
    what += String::convert ( size );
    what += ").";
    throw runtime_error ( what );
  }
}

// returns dm in both cases: get
// why property? - white spaces

  inline int DataSourceController::t_action (int state, int token) const
  {
    const int yyn = action_index [state] + token;

    if (yyn < 0 || action_check [yyn] != token)
      return action_default [state];

    return action_info [yyn];
  }



// why command
// no dm written, no dm calls

void
FitsController::
checkForImage ( PlotterBase * plotter, const DataSource & source,
		const std::vector < std::string > & binding )
{
  const FitsFile * file = 0;
  try {
    const FitsNTuple & ntuple 
      = dynamic_cast < const  FitsNTuple & > ( source );
    file = ntuple.getFile ();
  }
  catch ( ... ) {
    // do nothing
  }
  if ( file == 0 ) return;

  FitsFileBase::HduType type = file -> getHduType ();
  if ( type != FitsFileBase::Image ) return;

  vector < long > sizes;
  file -> fillAxisSizes ( sizes );
  if ( sizes.size () != 2 ) {
    assert ( sizes[2] == 1 );
  }
  plotter -> setNumberOfBins ( Axes::X, sizes[0] );
  plotter -> setNumberOfBins ( Axes::Y, sizes[1] );

  vector < double > deltas;
  file -> fillImageDeltas ( deltas );
  plotter -> setBinWidth ( Axes::X, deltas[0] );
  plotter -> setBinWidth ( Axes::Y, deltas[1] );

  vector < double > ref_values;
  file -> fillRefPixelValues ( ref_values );
  vector < int > ref_indices;
  file -> fillRefPixelIndices ( ref_indices );

  double x_orig = - deltas[0] * ( ref_indices[0] -1 ) + ref_values[0];
  double y_orig = - deltas[1] * ( ref_indices[1] -1 ) + ref_values[1];
  plotter ->setOffset ( Axes::X, x_orig );
  plotter ->setOffset ( Axes::Y, y_orig );

  Range range;
  if ( deltas[0] < 0. ) {
    range.setLow ( x_orig + ( sizes[0] + 1 ) * deltas[0] );
    range.setHigh ( x_orig );
  }
  else {
    range.setLow ( x_orig );
    range.setLength ( ( sizes[0] + 1 ) * deltas[0] ) ;
  }
  plotter -> setRange ( Axes::X, range, false, true );
  range.setLow ( y_orig );
  range.setLength ( ( sizes[1] + 1 ) * deltas[1] );
  plotter -> setRange ( Axes::Y, range, false, true );

  plotter -> matrixTranspose ( true );

  bool yes = file -> isHammerAitoff ();
  if ( yes ) {
    plotter ->setAspectRatio ( 2.0 );
  }
}

//??????? 1 dm assignment but 2 calls (1 call in condition ) 
// allow to have any number of calls in conditions for set ?

bool
DataSource::
setLabelAt( const std::string & s, unsigned int i )
{
  if ( i >= m_labels.size() ) return false;
  m_labels[i] = s;
  notifyObservers ();

  return true;
}
