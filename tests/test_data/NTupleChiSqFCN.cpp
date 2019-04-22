/* -*- mode: c++ -*- */

/** @file

hippodraw::NTupleChiSqFCN class interface

Copyright (C) 2003-2006   The Board of Trustees of The Leland Stanford
Junior University.  All Rights Reserved.

$Id: NTupleChiSqFCN.h,v 1.13 2006/01/08 19:21:48 pfkeb Exp $

*/

#ifndef _NTupleChiSqFCN_H_
#define _NTupleChiSqFCN_H_

#include "NTupleFCN.h"

namespace hippodraw {

/** A Chi-squared functor class.  A Chi-squared objective function
    functor class compatible with C++ version of @em Minuit.  This
    class gets its data points from a DataSource provided by a
    ProjectorBase object.  It uses functions derived from
    FunctionBase.

    @author Paul F. Kunz <Paul_Kunz@slac.stanford.edu>
*/

class MDL_HIPPOPLOT_API NTupleChiSqFCN : public NTupleFCN
{

private:

  /** The copy constructor. */
  NTupleChiSqFCN ( const NTupleChiSqFCN & );

public:

  /** The default constructor.
   */
  NTupleChiSqFCN ();

  /** Makes a copy of the object. */
  virtual StatedFCN * clone () const;

#ifdef HAVE_MINUIT2
  virtual double Up () const;
#else
  virtual double up () const;
#endif
  /** Calculates and returns the Chi-Squared.  This objective function
      object compares the function with the data points and returns
      the Chi-Squared.  If any data points has error measurement, then
      data points with zero error measurement are ignored.  If none of
      the data points have error measurement, then an error of 1.0 is
      used.
   */
  virtual double objectiveValue () const;
  virtual bool needsIntegrated () const;

};

} // namespace hippodraw

#endif // _NTupleChiSqFCN_H_

/** @file

hippodraw::NTupleFCN class implemenation.

Copyright (C) 2003-2006   The Board of Trustees of The Leland Stanford
Junior University.  All Rights Reserved.

$Id: NTupleFCN.cxx,v 1.49 2006/08/16 21:51:06 pfkeb Exp $

*/

#ifdef _MSC_VER
#include "msdevstudio/MSconfig.h"
#endif

#include "NTupleFCN.h"

#include "datasrcs/DataPointTuple.h"
#include "datasrcs/DataSource.h"
#include "datasrcs/TupleCut.h"

#include "functions/FunctionBase.h"

#include <algorithm>
#include <functional>

using std::bind2nd;
using std::count;
using std::find_if;
using std::not_equal_to;
using std::vector;

using namespace hippodraw;

NTupleFCN::
NTupleFCN ( )
  :  m_fit_cut ( 0 ),
     m_ntuple ( 0 ),
     m_has_errors ( false ),
     m_fit_range ( false )
{
}

NTupleFCN::
NTupleFCN ( const NTupleFCN & fcn )
  : StatedFCN ( fcn ),
    m_fit_cut ( 0 ),
    m_ntuple ( fcn.m_ntuple ),
    m_has_errors ( fcn.m_has_errors ),
    m_fit_range ( fcn.m_fit_range )
{
}

void
NTupleFCN::
copyFrom ( const StatedFCN * base )
{
  StatedFCN::copyFrom ( base );

  const NTupleFCN * fcn = dynamic_cast < const NTupleFCN * > ( base );
  if ( fcn != 0 ) {
    m_fit_cut    = fcn -> m_fit_cut;
    m_fit_range  = fcn -> m_fit_range;
    m_indices    = fcn -> m_indices;
    m_ntuple     = fcn -> m_ntuple;
    m_has_errors = fcn -> m_has_errors;
  }
}

namespace dp2 = hippodraw::DataPoint2DTuple;
namespace dp3 = hippodraw::DataPoint3DTuple;

void
NTupleFCN::
setDataSource ( const DataSource * ntuple )
{
  unsigned int size = ntuple -> columns ();
  vector < int > indices ( size );

  for ( unsigned int i = 0; i < size; i++ ) {
    indices [i] = i;
  }

  setDataSource ( ntuple, -1, indices );
}

void
NTupleFCN::
setDataSource ( const DataSource * ntuple, 
		int dimension,
		const std::vector < int > & indices )
{
  m_ntuple = ntuple;
  m_indices = indices;
}

int
NTupleFCN::
getErrorColumn () const
{
  unsigned int dim = ( m_indices.size() -2 ) / 2;
  int ie = m_indices [ 2 * dim + 1 ];

  return ie;
}

bool
NTupleFCN::
hasErrors ( ) const
{
  bool yes = false;

  unsigned int ie = getErrorColumn ();
  unsigned int cols = m_ntuple -> columns ();
  if ( ie < cols ) {
    const vector < double > & errors = m_ntuple -> getColumn ( ie );

    if ( errors.empty() ) return false;

    vector < double >::const_iterator first
      = find_if ( errors.begin(), errors.end (),
		  bind2nd ( not_equal_to < double > (), 0.0 ) );
    
    yes = first != errors.end ();
  }

  return yes;
}

bool
NTupleFCN::
setUseErrors ( bool yes )
{
  bool didit = false;
  if ( yes ) {
    if ( hasErrors () ) {
      m_has_errors = true;
      didit = true;
    }
    else m_has_errors = false;
  }
  else {
    m_has_errors = false;
      didit = true;
  }
  return didit;
}

bool
NTupleFCN::
getUseErrors () const
{
  return m_has_errors;
}

int
NTupleFCN::
degreesOfFreedom () const
{
  int ie = getErrorColumn ();

  const vector < double > & errors = m_ntuple -> getColumn ( ie );
  int number_points = errors.size();
  if ( m_has_errors ) {
    int zeros = count ( errors.begin(), errors.end(), 0.0 );
    number_points -= zeros;
  }

  vector< double > free_parms;
  return number_points - getNumberFreeParms ();
}

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

/** @bug Following only works for 1 dimension coordinate.
 */
void
NTupleFCN::
calcAlphaBeta ( std::vector < std::vector < double > > & alpha,
		std::vector < double > & beta )
{
  int ix = m_indices [ dp2::X ];
  int iy = m_indices [ dp2::Y ];
  int ie = m_indices [ dp2::YERR ];
  unsigned int num_parms = getNumberFreeParms ();
  reset ( alpha, beta, num_parms );

  unsigned int rows = m_ntuple -> rows ();
  for ( unsigned int i = 0; i < rows; i++ ) {
    if ( acceptRow ( i ) ) {
      const vector < double > & row = m_ntuple -> getRow ( i );

      double err = ie < 0 ? 0. : row [ ie ];
      if ( err == 0.0 && m_has_errors ) continue;
      if ( m_has_errors == false ) err = 1.0;

      double x = row [ ix ];
      double y = row [ iy ];

      double y_diff = y - m_function -> operator () ( x );
      vector < double > derives;
      fillFreeDerivatives ( derives, x );

      for ( unsigned int j = 0; j < num_parms; j++ ) {
	double t = derives[j] / ( err * err );

	for ( unsigned int k = 0; k <= j; k++ ) {
	  alpha[j][k] = alpha[j][k] + t * derives[k];
	}

	beta[j] += t * y_diff;
      }
    }
  }
}

/** @bug Works only for one dimensional coordinate.
 */
void
NTupleFCN::
setFitCut ( TupleCut * cut )
{
  m_fit_cut = cut;

  if ( cut != 0 ) {
    int ix = m_indices [ dp2::X ];
    cut -> setColumn ( ix );
  }
}

void
NTupleFCN::
setFitRange ( bool yes )
{
  m_fit_range = yes;
}

bool
NTupleFCN::
acceptRow ( unsigned int row ) const
{
    bool yes = true;
    if ( m_fit_cut != 0 &&
	 m_fit_cut -> isEnabled () &&
	 m_fit_range ) {
      yes = m_fit_cut -> acceptRow ( m_ntuple, row );
    }

    return yes;
}
