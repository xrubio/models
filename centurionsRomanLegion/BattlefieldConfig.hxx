
#ifndef __BattlefieldConfig_hxx__
#define __BattlefieldConfig_hxx__

#include <Config.hxx>
#include <Size.hxx>
#include <string>
#include <list>

class TiXmlElement;

namespace ClassicalWarfare 
{
class Battlefield;

struct Line
{
	int _numBlocks;
	int _ranks;
	int _columns;
	int _separationBetweenBlocks;
	int _offset;
};

enum CenturionPosition
{
	eRandom = 0,
	eRandomFirstLine = 1,
	eRightFirstLine = 2
};

class BattlefieldConfig : public Engine::Config
{
	void loadParams();

	void loadArmy(const std::string & tag, bool isRed);
public:
	// distance between opponent battle lines at the beginning of the simulation
	int _initialDistance;
	// distance at which a warrior can kill an enemy
	int _killingZone;
	// ranged lethality
	int _rangedLethality;
	// close combat lethality
	int _closeCombatLethality;

	int _redSeparationBetweenLines;
	float _redStressThreshold;
	float _redCenturionFactor;
	std::list<Line> _redLines;

	int _blueSeparationBetweenLines;
	float _blueStressThreshold;
	float _blueCenturionFactor;
	std::list<Line> _blueLines;

	CenturionPosition _redCenturionPosition;
	CenturionPosition _blueCenturionPosition;

public:
	BattlefieldConfig( const std::string & fileName );
	virtual ~BattlefieldConfig();

	friend class Battlefield;
};

} // namespace ClassicalWarfare

#endif // __BattlefieldConfig_hxx__

