/*********************************************************************
* Software License Agreement (BSD License)
*
*  Copyright (c) 2008, Willow Garage, Inc.
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions
*  are met:
*
*   * Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*   * Redistributions in binary form must reproduce the above
*     copyright notice, this list of conditions and the following
*     disclaimer in the documentation and/or other materials provided
*     with the distribution.
*   * Neither the name of the Willow Garage nor the names of its
*     contributors may be used to endorse or promote products derived
*     from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*********************************************************************/

/** \author Ioan Sucan
*  \author Guillaume Walck
* */

#include <gtest/gtest.h>
#include <cstdlib>

#include <dirent.h>
#include <sys/types.h>
#include <sys/param.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <string>

#include <iostream>

int runExternalProcess(const std::string &executable, const std::string &args)
{
  return system((executable + " " + args).c_str());
}

std::string getCommandOutput(std::string cmd)
{
  std::string data;
  FILE * stream;

  stream = popen(cmd.c_str(), "r");
  if (stream)
  {
    char buffer[MAXPATHLEN];
    while (!feof(stream))
      if (fgets(buffer, MAXPATHLEN, stream) != NULL) data.append(buffer);
    pclose(stream);
  }
  // keep anything before first cr/lf
  unsigned pos = data.find_first_of('\n');
  return data.substr(0, pos);
}

int walker(std::string &result, int &test_result)
{
  std::string package_path =  getCommandOutput("rospack find sr_description");

  if (package_path.find("sr_description") == std::string::npos)
  {
    printf("cannot find package in path %s\n", package_path.c_str());
    test_result = 1;
    return 1;
  }
  else
  {
    printf("sr_description robots path : %s\n", (package_path+"/robots").c_str());
  }

  DIR           *d;
  struct dirent *dir;
  d = opendir((package_path+"/robots").c_str());
  if (d == NULL)
  {
    printf("no robots found\n");
    test_result = 1;
    return 1;
  }
  while ((dir = readdir(d)))
  {
    if (strcmp(dir->d_name, ".") == 0 ||
        strcmp(dir->d_name, "..") == 0)
    {
      continue;
    }
    if (dir->d_type != DT_DIR)
    {
      std::string dir_name = dir->d_name;
      if (dir_name.find(std::string(".urdf.xacro")) == dir_name.size()-11)
      {
        std::string name = package_path + "/robots/" + dir_name;
        printf("\n\ntesting: %s\n", name.c_str());
        printf("xacro %s  > %s/test/tmp.urdf\n", name.c_str(), package_path.c_str());
        result += name;
        result += " ";
        runExternalProcess("xacro", name + " > " + package_path + "/test/tmp.urdf");
        // check urdf structure
        test_result = test_result || runExternalProcess("check_urdf", package_path + "/test/tmp.urdf");
      }
      if (test_result != 0)
        return test_result;
    }
  }
  closedir(d);
  return test_result;
}

TEST(URDF, CorrectFormat)
{
  int test_result = 0;

  std::string result;
  if (walker(result, test_result) == 0)
  {
    printf("Found: %s\n", result.c_str());
  }
  else
  {
    puts("Not found");
    test_result = -1;
  }

  EXPECT_EQ(test_result, 0);
}

int main(int argc, char **argv)
{
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
