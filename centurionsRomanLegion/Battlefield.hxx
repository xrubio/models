
#ifndef __Battlefield_hxx
#define __Battlefield_hxx

#include <World.hxx>
#include "BattlefieldConfig.hxx"

namespace ClassicalWarfare
{

class BattlefieldConfig;

enum Rasters
{
	eRedCloseCombat,
	eBlueCloseCombat,
	eRedRanged,
	eBlueRanged
};

class Line;

class Battlefield : public Engine::World
{
	void createRasters();
	void createAgents();
	void createLine( const Line & line, int depth, bool isRed, int & createdLegionaries, int & createdCenturions, const CenturionPosition & centurionPosition);
	bool isCenturionPosition( const Engine::Point2D<int> & position, const Line & line, const CenturionPosition & centurionPosition) const;
	
	void stepEnvironment();

public:
	Battlefield( BattlefieldConfig * config, Engine::Scheduler * scheduler = 0);
	virtual ~Battlefield();
};

} // namespace ClassicalWarfare 

#endif // __Battlefield_hxx

