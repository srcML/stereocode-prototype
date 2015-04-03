// ---------------- get + property

// ?? property (only dm are returned in both returns) - should be get

 inline int DataSourceController::t_action (int state, int token) const
  {
    const int yyn = action_index [state] + token;

    if (yyn < 0 || action_check [yyn] != token)
      return action_default[state];

    return action_info[yyn];
  }
  
 // could be like this  

 inline int DataSourceController::t_action (int state, int token) const
  {
    const int yyn = action_index[state] + token;

    if (yyn < 0 || action_check[yyn] != token)
      return - action_default[state]; //returns some calculation on dm

    return action_info[yyn]; //returnd dm
  }

// should be get: return dm or literal   

const CFuzzyElement CFuzzyMembershipFunction::FindVertex (long key) const
{
  for (long i=0; i < GetNumVertices(); i++)
  {
    //CFuzzyElement FE;
    GetVertex(i,&FE);
    if (FE.GetValue() == key)
    {
      return FE;
    }
  }

  return -1;
}  



// ---------------------- not commands  

// why command - know the problem you mentioned (casting)
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

// no dm-calls, no dm-assignment => why command?  
int
NTupleController::
createNTupleToFile( const std::vector < std::string > & column_list,
		    const std::vector < const TupleCut * > & cut_list, 
		    DataSource * ds,
		    const std::string & filename,
		    const std::string & dsname)
{
  if ( column_list.empty() ) return 1;

  ofstream file ( filename.c_str() );
  if ( file.is_open () == false ) {
    return 1;
  }
  // Check the column list and create indices for inner loop
  unsigned int columnNumber = column_list.size();
  vector < int > col_indices ( columnNumber );
  
  for ( unsigned int i = 0; i < columnNumber; i++ ) {
    const string & label = column_list [ i ];
    int index = ds -> indexOf ( label );
    if ( index < 0 ) { 
     ds -> throwIfInvalidLabel ( label );
    }
    col_indices [i] = index;
  }

  file << dsname << endl;

#ifdef ITERATOR_MEMBER_DEFECT
  std::
#endif
  vector < string > ::const_iterator first = column_list.begin ();
  string label = *first++;
  file << label;
  while (  first != column_list.end() ) {
    label = *first++;
    file << "\t" << label;
  }
  file << endl;

  unsigned int cutNumber = cut_list.size();
  unsigned int size = ds->rows();

   // Check all the rows.
  for ( unsigned int i = 0; i < size; i++ )
    {
      // If cut is not selected, default is accept.
      bool accept = true;

      // Check all the cuts.
      for ( unsigned int j = 0; j < cutNumber; j++ ) 
	{
	  const TupleCut * tc = cut_list[j];
	  accept = tc -> acceptRow ( ds, i );
	  if (!accept) break;
	}
      
      // Add the row to the file when all cuts accept the row.
      if (accept) {
	
	for ( unsigned int k = 0; k < columnNumber; k++ ) 
	  {
	    int index = col_indices [ k ];
	    file << "\t" << ds -> valueAtNoCache (i, index );	    
	  }
	file << endl;
      }
    }
  return 0; 
}

//why command?
//should be COLLAB-COmmand (command because of DataSourceController::instance () -? )

string
NTupleController::
registerNTuple ( DataSource * ds )
{
  DataSourceController * controller = DataSourceController::instance ();
  controller -> registerNTuple ( ds );

  return ds -> getName ();
}  


// ----------------- set + command

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

bool CFuzzySetRelation::SetValue (long col, long row, double value)
{
  long NumRows    = m_RowHeadings.GetNumFuzzyElements();
  long NumColumns = m_ColumnHeadings.GetNumFuzzyElements();

  if ((0 <= col) && (col < NumColumns) && (0 <= row) && (row < NumRows) && (0.0 <= value) && (value <= 1.0))
  {
    m_pData[col][row] = value;
    return true;
  }

  return false;
}



//---------------- factory


// it's ok

ProjectorBase *
TextDataRep::
getTargetProjector ( ) const
{
  ProjectorBase * projector = 0;
  DataRep * target = getParentDataRep();

  if ( target != 0 ) {
    projector = target -> getProjector ();
  }

  return projector;
}


//  -------------- collabor-coomand + command or collabor-coomand + non-void command
//why COLLABORATIONAL COMMAND  
void EpsView::initPlot ( const std::string & fname, 
			 double x, double y, double w, double h )
{

  const char * fn = fname.c_str();
  m_outfile.open (fn, std::ios::out); //call on dm

  m_outfile << "%%!PS-Adobe-3.0 EPSF-3.0" << endl;
  m_outfile << "%%Creator: HippoPlot" << endl;

  double x1 = x;
  double y1 = y;
  double x2 = x + w;
  double y2 = y + h;

  m_outfile << "%%BoundingBox: " 
	  << x1 << " " << y1 << " " 
	  << x2 << " " << y2 << endl; 
  
  m_outfile << "%%EndComments" << endl;
  m_outfile << endl << endl;

  m_outfile << "%% Add emulation of selectfont if needed" << endl;
  m_outfile << "%%   taken from PS Lang. Ref. Manual, Appendix D.4" << endl;
  m_outfile << "/*SF {" << endl;
  m_outfile << "  exch findfont exch" << endl;
  m_outfile << "  dup type /arraytype eq {makefont}{scalefont} ifelse setfont" 
	    << endl;
  m_outfile << "} bind def" << endl;
  m_outfile << endl;
  m_outfile << "/languagelevel where" << endl;
  m_outfile << " {pop languagelevel} {1} ifelse" << endl;
  m_outfile << "2 lt {/SF /*SF load def}{/SF /selectfont load def} ifelse"
	  << endl;

  m_outfile << "%%" << endl << "%%" << endl;
}



// but:
// WHY IT'S NOT COLLABORATOR ? 
void EpsView::drawLines ( const std::vector< double > & x,
			  const std::vector< double > & y,
			  hippodraw::Line::Style style,
			  const Color & color,
			  float size )
{
  m_outfile << "%% drawLines" << endl;

  m_outfile << "gsave" << endl;

  m_outfile << (float)(color.getRed() / 255.0) << " " 
	  << (float)(color.getGreen() / 255.0) << " "
	  << (float)(color.getBlue() / 255.0) << " setrgbcolor" << endl;

  m_outfile << size << " setlinewidth" << endl;

  switch (style)
    {
    case Line::Solid:
      m_outfile << "[] 0 setdash" << endl;
      break;
    case Line::Dot:
      m_outfile << "[3 5] 0 setdash" << endl;
      break;
    case Line::Dash:
      m_outfile << "[5 3] 0 setdash" << endl;
      break;
    case Line::DashDot:
      m_outfile << "[5 3 1 3] 0 setdash" << endl;
      break;
    default:
      break;
    }
  
  for ( unsigned int i = 0; i < x.size(); i = i+2 )
    {
      
      m_outfile << "gsave" << endl << "newpath systemdict begin" << endl;
      m_outfile << toViewX (x[i]) << " "
	      << toViewY (y[i]) << " moveto" << endl;
      m_outfile << toViewX (x[i+1]) << " "
	      << toViewY (y[i+1]) << " lineto" << endl;
      m_outfile << "end" << endl;
      m_outfile << "stroke grestore" << endl;
      
    }

  m_outfile << "grestore" << endl;

}

//why command
void 
NTupleFCN::
reset ( std::vector < std::vector < double > > & alpha,
	std::vector < double > & beta,
	unsigned int size )
{
  beta.clear ();
  beta.resize ( size, 0.0 );

  alpha.resize ( size );

  for ( unsigned int i = 0; i < alpha.size (); i++ ) {
    alpha[i].clear ();
    alpha[i].resize ( size, 0.0 );
  }
}

// why command? - argv[0] as dm 
void HdThread::run ()
{
  static int argc = 1;
  static char * argv[1];
  argv[0] = "HippoDraw";

  QtApp app ( argc, argv );
  app.setFirstWindow();

  try {
    app.exec ();
  }
  catch ( std::exception & e ) {
    std::cout << e.what()
	      << std::endl;
  }
}

// why collaborational-command?
void
QtFont::
setFamily ( const std::string & family )
{
  m_font.setFamily( family.c_str() );
}

//why COLLLAB-COMMAND?
/** 4) @stereotype  */
XmlDocument::Status
QtXmlDocument::
saveToFile ( const std::string & filename )
{
  QFile filedev ( filename.c_str() );

  bool ok = filedev.open ( IO_WriteOnly );
  if ( ! ok ) {
    return WriteError;
  }

  QTextStream ts ( &filedev );
  m_document.save ( ts, 2 ); //dm.call()
  filedev.close ();

  return Success;
}





  
//------------------ some others issues  
//1) 
//why not stateless?
//call in expr is not counted 
string::size_type NTupleController::findWhite ( const std::string & line, unsigned int left, bool tabs_only )
{
 line.find( '\t', left );

  return right;
}

//vs stateless
// call in return is counted
string::size_type NTupleController::findWhite ( const std::string & line, unsigned int left, bool tabs_only )
{
  return line.find( '\t', left );;
} 

// 2) not very important - can leave for now?
// ----------------- unclassified 


void EpsView::endPlot()
{
  m_outfile << "%%EOF" << endl;
}

void
DataSourceController::
checkWidth ( const DataSource * source )
{
  throw runtime_error ( what );
}
