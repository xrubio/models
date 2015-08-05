
#include <Exception.hxx>
#include <iostream>
#include <cstdlib>

#include "Battlefield.hxx"
#include "BattlefieldConfig.hxx"

int main(int argc, char *argv[])
{
	try
	{
		if(argc>2)
		{
			throw Engine::Exception("USAGE: legion [config file]");
		}
		
		std::string fileName("config.xml");
		if(argc!=1)
		{
			fileName = argv[1];
		}
		ClassicalWarfare::Battlefield battle( new ClassicalWarfare::BattlefieldConfig(fileName),battle.useOpenMPSingleNode());
		battle.initialize(argc, argv);
		battle.run();
	}
	catch( std::exception & exceptionThrown )
	{
		std::cout << "exception thrown: " << exceptionThrown.what() << std::endl;
	}
	return 0;
}

