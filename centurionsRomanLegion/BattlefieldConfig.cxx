
#include "BattlefieldConfig.hxx"

namespace ClassicalWarfare
{

BattlefieldConfig::BattlefieldConfig( const std::string & fileName ) : Config(fileName), _initialDistance(9), _redSeparationBetweenLines(0), _blueSeparationBetweenLines(0)
{
}

void BattlefieldConfig::loadArmy( const std::string & tag, bool isRed)
{
	if(isRed)
	{
		_redSeparationBetweenLines = getParamInt(tag, "separationBetweenLines");
		_redStressThreshold = getParamFloat(tag, "stressThreshold");
		_redCenturionFactor = getParamFloat(tag, "centurionFactor");
		_redCenturionPosition = (CenturionPosition)getParamInt(tag, "centurionPosition");
	}
	else
	{
        _blueSeparationBetweenLines = getParamInt(tag, "separationBetweenLines");
		_blueStressThreshold = getParamFloat(tag, "stressThreshold");
		_blueCenturionFactor = getParamFloat(tag, "centurionFactor");
		_blueCenturionPosition = (CenturionPosition)getParamInt(tag, "centurionPosition");
	}

    // TODO more tha one line?
    std::stringstream lineTag;
    lineTag << tag << "/line";
    Line lineConfig;
    lineConfig._ranks = getParamInt(lineTag.str(), "ranks");
    lineConfig._numBlocks = getParamInt(lineTag.str(), "numBlocks");
    lineConfig._columns = getParamInt(lineTag.str(), "columns");
    lineConfig._separationBetweenBlocks = getParamInt(lineTag.str(), "separationBetweenBlocks");
    lineConfig._offset = getParamInt(lineTag.str(), "offset");

    if(isRed)
    {
        _redLines.push_back(lineConfig);
    }
    else
    {
        _blueLines.push_back(lineConfig);
    }
}

void BattlefieldConfig::loadParams()
{
    _initialDistance = getParamInt("battlefield", "initialDistance");
    _killingZone = getParamInt("dynamics", "killingZone");
    _rangedLethality = getParamInt("dynamics", "rangedLethality");
    _closeCombatLethality = getParamInt("dynamics", "closeCombatLethality");

	loadArmy("redArmy", true);
	loadArmy("blueArmy", false);
}

BattlefieldConfig::~BattlefieldConfig()
{
}

} // namespace ClassicalWarfare

