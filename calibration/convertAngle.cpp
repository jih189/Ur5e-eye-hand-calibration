#include<iostream>
#include<visp3/core/vpQuaternionVector.h>
#include<visp3/core/vpThetaUVector.h>
#include<string>
int main(int argc, char** argv)
{

    std::string::size_type sz;

    if(argc != 5){
        std::cout << "need 4 arguments\n";
        return 1;
    }
    float x, y, z, w;
    std::cout << "x:" << argv[1] << std::endl;
    x = std::stof(argv[1], &sz);
    std::cout << "y:" << argv[2] << std::endl;
    y = std::stof(argv[2], &sz);
    std::cout << "z:" << argv[3] << std::endl;
    z = std::stof(argv[3], &sz);
    std::cout << "w:" << argv[4] << std::endl;
    w = std::stof(argv[4], &sz);
    vpQuaternionVector vp(x,y,z,w);
    vpThetaUVector tuv(vp);
    std::cout << "result:\n";
    std::cout << tuv << std::endl;
    std::cout << "copy following data and append them to yaml file\n";
    std::cout << "  - [" << tuv[0] << "]" << std::endl;
    std::cout << "  - [" << tuv[1] << "]" << std::endl;
    std::cout << "  - [" << tuv[2] << "]" <<  std::endl;
    return 0;
}

