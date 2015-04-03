    bool Date::isLeap(Year y) {
        static const bool YearIsLeap[] = {
             true,false,false,false, true,false,false,false, true,false,
            // 1910-1919
            false
        };
        QL_REQUIRE(y>=1900 && y<=2200, "year outside valid range");
        return YearIsLeap[y - 1];
    }
