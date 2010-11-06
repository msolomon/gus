/*
  Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.

  The MySQL Connector/C++ is licensed under the terms of the GPLv2
  <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
  MySQL Connectors. There are special exceptions to the terms and
  conditions of the GPLv2 as it is applied to this software, see the
  FLOSS License Exception
  <http://www.mysql.com/about/legal/licensing/foss-exception.html>.

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published
  by the Free Software Foundation; version 2 of the License.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
  for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA
*/

#include "../framework/test_runner.h"
#include "../framework/start_options.h"
#include "../framework/test_tapOutputter.h"
#include "../framework/test_filter.h"
#include <stdlib.h>

int main(int argc, char** argv)
{
  const String::value_type * unnamedStartParams[]= { "dbUrl"
    , "dbUser"
    , "dbPasswd"
    , "dbSchema"
    , NULL };

  Properties defaultStringValues;

  defaultStringValues.insert( Properties::value_type( "dbUrl"   , "tcp://127.0.0.1:3306" ) );
  defaultStringValues.insert( Properties::value_type( "dbUser"  , "root" ) );
  defaultStringValues.insert( Properties::value_type( "dbPasswd", "root" ) );
  defaultStringValues.insert( Properties::value_type( "dbSchema", "test" ) );
  defaultStringValues.insert( Properties::value_type( "filter"  , "" ) );

  std::map<String, bool> defaultBoolValues;

  testsuite::StartOptions options( unnamedStartParams, & defaultStringValues
    , & defaultBoolValues );

  options.parseParams( argc, argv );

  testsuite::FiltersSuperposition filter( options.getString( "filter" ) );



  /*
  std::cerr << "BlobTest: "
      << (filter.Admits( "BlobTest" ) ? "Admitted" : "Filtered Out" )
      << std::endl;

    return 0;*/

/*std::cerr << options.getString( "dbUrl" ) << std::endl;
  std::cerr << options.getString( "dbUser" ) << std::endl;
  std::cerr << options.getString( "dbPasswd" ) << std::endl;
  std::cerr << options.getString( "dbSchema" ) << std::endl;
  std::cerr << options.getBool( "verbose" ) << std::endl;
  std::cerr << options.getBool( "timer" ) << std::endl;
  std::cerr << options.getBool( "dont-use-is" ) << std::endl;

  return 0;*/


  testsuite::TestsRunner & testsRunner=testsuite::TestsRunner::theInstance();

  testsRunner.setStartOptions ( & options );
  testsRunner.setTestsFilter  ( filter    );

  return testsRunner.runTests() ? EXIT_SUCCESS : EXIT_FAILURE;
}
