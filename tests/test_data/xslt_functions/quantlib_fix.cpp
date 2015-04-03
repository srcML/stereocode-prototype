// combinations of collaborational-command with command/non-void command


// non-void command + collaborational-command

	/** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    std::string IMM::code(const Date& date) {
        QL_REQUIRE(isIMMdate(date, false),
                   date << " is not an IMM date");

        std::ostringstream IMMcode;
        unsigned int y = date.year() % 10;
        switch(date.month()) {
          case January:
            IMMcode << 'F' << y;
            break;
          case February:
            IMMcode << 'G' << y;
            break;
          case March:
            IMMcode << 'H' << y;
            break;
          case April:
            IMMcode << 'J' << y;
            break;
          case May:
            IMMcode << 'K' << y;
            break;
          case June:
            IMMcode << 'M' << y;
            break;
          case July:
            IMMcode << 'N' << y;
            break;
          case August:
            IMMcode << 'Q' << y;
            break;
          case September:
            IMMcode << 'U' << y;
            break;
          case October:
            IMMcode << 'V' << y;
            break;
          case November:
            IMMcode << 'X' << y;
            break;
          case December:
            IMMcode << 'Z' << y;
            break;
          default:
            QL_FAIL("not an IMM month (and it should have been)");
        }

        #if defined(QL_EXTRA_SAFETY_CHECKS)
        QL_ENSURE(isIMMcode(IMMcode.str(), false),
                  "the result " << IMMcode.str() <<
                  " is an invalid IMM code");
        #endif
        return IMMcode.str();
    }

    /** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    Date IMM::date(const std::string& immCode,
                   const Date& refDate) {
        QL_REQUIRE(isIMMcode(immCode, false),
                   immCode << " is not a valid IMM code");

        Date referenceDate = (refDate != Date() ?
                              refDate :
                              Date(Settings::instance().evaluationDate()));

        std::string code = to_upper_copy(immCode);
        std::string ms = code.substr(0,1);
        QuantLib::Month m;
        if (ms=="F")      m = January;
        else if (ms=="G") m = February;
        else if (ms=="H") m = March;
        else if (ms=="J") m = April;
        else if (ms=="K") m = May;
        else if (ms=="M") m = June;
        else if (ms=="N") m = July;
        else if (ms=="Q") m = August;
        else if (ms=="U") m = September;
        else if (ms=="V") m = October;
        else if (ms=="X") m = November;
        else if (ms=="Z") m = December;
        else QL_FAIL("invalid IMM month letter");

        Year y = boost::lexical_cast<Year>(code.substr(1,1));
        /* year<1900 are not valid QuantLib years: to avoid a run-time
           exception few lines below we need to add 10 years right away */
        if (y==0 && referenceDate.year()<=1909) y+=10;
        Year referenceYear = (referenceDate.year() % 10);
        y += referenceDate.year() - referenceYear;
        Date result = IMM::nextDate(Date(1, m, y), false);
        if (result<referenceDate)
            return IMM::nextDate(Date(1, m, y+10), false);

        return result;
    }

    /** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    Date IMM::nextDate(const Date& date, bool mainCycle) {
        Date refDate = (date == Date() ?
                        Date(Settings::instance().evaluationDate()) :
                        date);
        Year y = refDate.year();
        QuantLib::Month m = refDate.month();

        Size offset = mainCycle ? 3 : 1;
        Size skipMonths = offset-(m%offset);
        if (skipMonths != offset || refDate.dayOfMonth() > 21) {
            skipMonths += Size(m);
            if (skipMonths<=12) {
                m = QuantLib::Month(skipMonths);
            } else {
                m = QuantLib::Month(skipMonths-12);
                y += 1;
            }
        }

        Date result = Date::nthWeekday(3, Wednesday, m, y);
        if (result<=refDate)
            result = nextDate(Date(22, m, y), mainCycle);
        return result;
    }

    /** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    Date IMM::nextDate(const std::string& IMMcode,
                       bool mainCycle,
                       const Date& referenceDate)  {
        Date immDate = date(IMMcode, referenceDate);
        return nextDate(immDate+1, mainCycle);
    }

    /** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    std::string IMM::nextCode(const Date& d,
                              bool mainCycle) {
        Date date = nextDate(d, mainCycle);
        return code(date);
    }

    /** @oldstereotype non-void-command collaborational-command collaborator */
    /** @stereotype non-void-command collaborator */
    std::string IMM::nextCode(const std::string& immCode,
                              bool mainCycle,
                              const Date& referenceDate) {
        Date date = nextDate(immCode, mainCycle, referenceDate);
        return code(date);
    }









// command + collaborational-command 


/** @oldstereotype command collaborational-command collaborator */
/** @stereotype command collaborator */
void AmericanOptionTest::testJuValues() {

    BOOST_MESSAGE("Testing Ju approximation for American options...");

    Date today = Date::todaysDate();
    DayCounter dc = Actual360();
    boost::shared_ptr<SimpleQuote> spot(new SimpleQuote(0.0));
    boost::shared_ptr<SimpleQuote> qRate(new SimpleQuote(0.0));
    boost::shared_ptr<YieldTermStructure> qTS = flatRate(today, qRate, dc);
    boost::shared_ptr<SimpleQuote> rRate(new SimpleQuote(0.0));
    boost::shared_ptr<YieldTermStructure> rTS = flatRate(today, rRate, dc);
    boost::shared_ptr<SimpleQuote> vol(new SimpleQuote(0.0));
    boost::shared_ptr<BlackVolTermStructure> volTS = flatVol(today, vol, dc);

    Real tolerance = 1.0e-3;

    for (Size i=0; i<LENGTH(juValues); i++) {

        boost::shared_ptr<StrikedTypePayoff> payoff(new
            PlainVanillaPayoff(juValues[i].type, juValues[i].strike));
        //FLOATING_POINT_EXCEPTION
        Date exDate = today + Integer(juValues[i].t*360+0.5);
        boost::shared_ptr<Exercise> exercise(
                                         new AmericanExercise(today, exDate));

        spot ->setValue(juValues[i].s);
        qRate->setValue(juValues[i].q);
        rRate->setValue(juValues[i].r);
        vol  ->setValue(juValues[i].v);

        boost::shared_ptr<BlackScholesMertonProcess> stochProcess(new
            BlackScholesMertonProcess(Handle<Quote>(spot),
                                      Handle<YieldTermStructure>(qTS),
                                      Handle<YieldTermStructure>(rTS),
                                      Handle<BlackVolTermStructure>(volTS)));

        boost::shared_ptr<PricingEngine> engine(
                            new JuQuadraticApproximationEngine(stochProcess));

        VanillaOption option(payoff, exercise);
        option.setPricingEngine(engine);

        Real calculated = option.NPV();
        Real error = std::fabs(calculated-juValues[i].result);
        if (error > tolerance) {
            REPORT_FAILURE("value", payoff, exercise, juValues[i].s,
                           juValues[i].q, juValues[i].r, today,
                           juValues[i].v, juValues[i].result,
                           calculated, error, tolerance);
        }
    }
}


/** @oldstereotype command collaborational-command collaborator */
/** @stereotype command collaborator */
void AmericanOptionTest::testFdValues() {

    BOOST_MESSAGE("Testing finite-difference engine for American options...");

    Date today = Date::todaysDate();
    DayCounter dc = Actual360();
    boost::shared_ptr<SimpleQuote> spot(new SimpleQuote(0.0));
    boost::shared_ptr<SimpleQuote> qRate(new SimpleQuote(0.0));
    boost::shared_ptr<YieldTermStructure> qTS = flatRate(today, qRate, dc);
    boost::shared_ptr<SimpleQuote> rRate(new SimpleQuote(0.0));
    boost::shared_ptr<YieldTermStructure> rTS = flatRate(today, rRate, dc);
    boost::shared_ptr<SimpleQuote> vol(new SimpleQuote(0.0));
    boost::shared_ptr<BlackVolTermStructure> volTS = flatVol(today, vol, dc);

    Real tolerance = 8.0e-2;

    for (Size i=0; i<LENGTH(juValues); i++) {

        boost::shared_ptr<StrikedTypePayoff> payoff(new
            PlainVanillaPayoff(juValues[i].type, juValues[i].strike));

        // FLOATING_POINT_EXCEPTION
        Date exDate = today + Integer(juValues[i].t*360+0.5);
        boost::shared_ptr<Exercise> exercise(
                                         new AmericanExercise(today, exDate));

        spot ->setValue(juValues[i].s);
        qRate->setValue(juValues[i].q);
        rRate->setValue(juValues[i].r);
        vol  ->setValue(juValues[i].v);

        boost::shared_ptr<BlackScholesMertonProcess> stochProcess(new
            BlackScholesMertonProcess(Handle<Quote>(spot),
                                      Handle<YieldTermStructure>(qTS),
                                      Handle<YieldTermStructure>(rTS),
                                      Handle<BlackVolTermStructure>(volTS)));

        boost::shared_ptr<PricingEngine> engine(
                                 new FDAmericanEngine(stochProcess, 100,100));

        VanillaOption option(payoff, exercise);
        option.setPricingEngine(engine);

        Real calculated = option.NPV();
        Real error = std::fabs(calculated-juValues[i].result);
        if (error > tolerance) {
            REPORT_FAILURE("value", payoff, exercise, juValues[i].s,
                           juValues[i].q, juValues[i].r, today,
                           juValues[i].v, juValues[i].result,
                           calculated, error, tolerance);
        }
    }
}


namespace {

    template <class Engine>
    void testFdGreeks() {

        SavedSettings backup;

        std::map<std::string,Real> calculated, expected, tolerance;
        tolerance["delta"]  = 7.0e-4;
        tolerance["gamma"]  = 2.0e-4;
        //tolerance["theta"]  = 1.0e-4;

        Option::Type types[] = { Option::Call, Option::Put };
        Real strikes[] = { 50.0, 99.5, 100.0, 100.5, 150.0 };
        Real underlyings[] = { 100.0 };
        Rate qRates[] = { 0.04, 0.05, 0.06 };
        Rate rRates[] = { 0.01, 0.05, 0.15 };
        Integer years[] = { 1, 2 };
        Volatility vols[] = { 0.11, 0.50, 1.20 };

        DayCounter dc = Actual360();
        Date today = Date::todaysDate();
        Settings::instance().evaluationDate() = today;

        boost::shared_ptr<SimpleQuote> spot(new SimpleQuote(0.0));
        boost::shared_ptr<SimpleQuote> qRate(new SimpleQuote(0.0));
        Handle<YieldTermStructure> qTS(flatRate(qRate, dc));
        boost::shared_ptr<SimpleQuote> rRate(new SimpleQuote(0.0));
        Handle<YieldTermStructure> rTS(flatRate(rRate, dc));
        boost::shared_ptr<SimpleQuote> vol(new SimpleQuote(0.0));
        Handle<BlackVolTermStructure> volTS(flatVol(vol, dc));

        boost::shared_ptr<StrikedTypePayoff> payoff;

        for (Size i=0; i<LENGTH(types); i++) {
          for (Size j=0; j<LENGTH(strikes); j++) {
            for (Size k=0; k<LENGTH(years); k++) {
                Date exDate = today + years[k]*Years;
                boost::shared_ptr<Exercise> exercise(
                                         new AmericanExercise(today, exDate));
                boost::shared_ptr<StrikedTypePayoff> payoff(
                                new PlainVanillaPayoff(types[i], strikes[j]));
                boost::shared_ptr<BlackScholesMertonProcess> stochProcess(
                            new BlackScholesMertonProcess(Handle<Quote>(spot),
                                                          qTS, rTS, volTS));

                boost::shared_ptr<PricingEngine> engine(
                                                    new Engine(stochProcess));

                VanillaOption option(payoff, exercise);
                option.setPricingEngine(engine);

                for (Size l=0; l<LENGTH(underlyings); l++) {
                  for (Size m=0; m<LENGTH(qRates); m++) {
                    for (Size n=0; n<LENGTH(rRates); n++) {
                      for (Size p=0; p<LENGTH(vols); p++) {
                        Real u = underlyings[l];
                        Rate q = qRates[m],
                             r = rRates[n];
                        Volatility v = vols[p];
                        spot->setValue(u);
                        qRate->setValue(q);
                        rRate->setValue(r);
                        vol->setValue(v);
                        //FLOATING_POINT_EXCEPTION
                        Real value = option.NPV();
                        calculated["delta"]  = option.delta();
                        calculated["gamma"]  = option.gamma();
                        //calculated["theta"]  = option.theta();

                        if (value > spot->value()*1.0e-5) {
                            // perturb spot and get delta and gamma
                            Real du = u*1.0e-4;
                            spot->setValue(u+du);
                            Real value_p = option.NPV(),
                                 delta_p = option.delta();
                            spot->setValue(u-du);
                            Real value_m = option.NPV(),
                                 delta_m = option.delta();
                            spot->setValue(u);
                            expected["delta"] = (value_p - value_m)/(2*du);
                            expected["gamma"] = (delta_p - delta_m)/(2*du);

                            /*
                            // perturb date and get theta
                            Time dT = dc.yearFraction(today-1, today+1);
                            Settings::instance().setEvaluationDate(today-1);
                            value_m = option.NPV();
                            Settings::instance().setEvaluationDate(today+1);
                            value_p = option.NPV();
                            Settings::instance().setEvaluationDate(today);
                            expected["theta"] = (value_p - value_m)/dT;
                            */

                            // compare
                            std::map<std::string,Real>::iterator it;
                            for (it = calculated.begin();
                                 it != calculated.end(); ++it) {
                                std::string greek = it->first;
                                Real expct = expected  [greek],
                                    calcl = calculated[greek],
                                    tol   = tolerance [greek];
                                Real error = relativeError(expct,calcl,u);
                                if (error>tol) {
                                    REPORT_FAILURE(greek, payoff, exercise,
                                                   u, q, r, today, v,
                                                   expct, calcl, error, tol);
                                }
                            }
                        }
                      }
                    }
                  }
                }
            }
          }
        }
    }

}























// factory +

/** @oldstereotype non-void-command collaborational-command collaborator factory */
/** @stereotype non-void-command collaborator factory */
test_suite* AmericanOptionTest::suite() {
    test_suite* suite = BOOST_TEST_SUITE("American option tests");
    suite->add(
        QUANTLIB_TEST_CASE(&AmericanOptionTest::testBaroneAdesiWhaleyValues));
    suite->add(
        QUANTLIB_TEST_CASE(&AmericanOptionTest::testBjerksundStenslandValues));
    // FLOATING_POINT_EXCEPTION
    suite->add(QUANTLIB_TEST_CASE(&AmericanOptionTest::testJuValues));
    // FLOATING_POINT_EXCEPTION
    suite->add(QUANTLIB_TEST_CASE(&AmericanOptionTest::testFdValues));
    // FLOATING_POINT_EXCEPTION
    suite->add(QUANTLIB_TEST_CASE(&AmericanOptionTest::testFdAmericanGreeks));
    // FLOATING_POINT_EXCEPTION
    suite->add(QUANTLIB_TEST_CASE(&AmericanOptionTest::testFdShoutGreeks));
    return suite;
}
