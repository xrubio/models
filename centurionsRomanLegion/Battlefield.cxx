
#include "Battlefield.hxx"
#include "BattlefieldConfig.hxx"

#include "Legionary.hxx"

#include <Agent.hxx>
#include <DynamicRaster.hxx>
#include <Point2D.hxx>
#include <Exception.hxx>
#include <Statistics.hxx>
#include <GeneralState.hxx>
#include <Rectangle.hxx>

#include <cmath>
#include <limits>

namespace ClassicalWarfare 
{
	
Battlefield::Battlefield( BattlefieldConfig * config, Engine::Scheduler * scheduler ) : World(config, scheduler, true)
{
}

Battlefield::~Battlefield()
{
}

void Battlefield::createRasters()
{
	registerDynamicRaster("redCloseCombatKills", true, eRedCloseCombat);
	registerDynamicRaster("blueCloseCombatKills", true, eBlueCloseCombat);
	getDynamicRaster(eRedCloseCombat).setInitValues(0, std::numeric_limits<int>::max(), 0);
	getDynamicRaster(eBlueCloseCombat).setInitValues(0, std::numeric_limits<int>::max(), 0);
	
	registerDynamicRaster("redRangedKills", true, eRedRanged);
	registerDynamicRaster("blueRangedKills", true, eBlueRanged);
	getDynamicRaster(eRedRanged).setInitValues(0, std::numeric_limits<int>::max(), 0);
	getDynamicRaster(eBlueRanged).setInitValues(0, std::numeric_limits<int>::max(), 0);
}

bool Battlefield::isCenturionPosition( const Engine::Point2D<int> & position, const Line & line, const CenturionPosition & centurionPosition) const
{
	if(centurionPosition==eRandom)
	{	
		// 1 centurion every 80 legionaries
		if(Engine::GeneralState::statistics().getUniformDistValue(1, 80)!=3)
		{
			return false;
		}
		return true;
	}
	// first and second century
	if(position._y!=0 && position._y!=8)
	{
		return false;
	}

	if(centurionPosition==eRandomFirstLine)
	{
		// 1 column of every set has a centurion
		if(Engine::GeneralState::statistics().getUniformDistValue(1, line._columns)!=3)
		{
			return false;
		}
		return true;
	}

	// historical: right first line
	if(position._x==line._columns-1)
	{
		return true;
	}
	return false;
}

void Battlefield::createLine( const Line & line, int depth, bool isRed, int & createdLegionaries, int & createdCenturions, const CenturionPosition & centurionPosition)
{
    const BattlefieldConfig & battleConfig = (const BattlefieldConfig &)getConfig();

	Engine::Point2D<int> blockPosition(0, depth);
	// we need to center the line
	int lineWidth = line._numBlocks*line._columns+(line._numBlocks-1)*line._separationBetweenBlocks;
	if(isRed)
	{
		blockPosition._x = (getBoundaries()._size._width-lineWidth)/2;
		blockPosition._x += line._offset*line._columns;
		blockPosition._x++;
	}
	else
	{
		blockPosition._x = getBoundaries()._size._width-(getBoundaries()._size._width-lineWidth)/2;
		blockPosition._x -= line._offset*line._columns;
	}

	for(int i=0; i<line._numBlocks; i++)
	{
		std::cout << "next block at pos: " << blockPosition << std::endl;
		Engine::Point2D<int> warriors(0,0);

		for(warriors._y=0; warriors._y<line._ranks; warriors._y++)
		{
			for(warriors._x=0; warriors._x<line._columns; warriors._x++)
			{
				bool isCenturion = isCenturionPosition(warriors, line, centurionPosition );
				std::ostringstream oss;
				float legionaryStress = battleConfig._redStressThreshold;
				float centurionStress = legionaryStress * battleConfig._redCenturionFactor;

				if(isRed)
				{
		 			oss << "Red";
				}
				else
				{	
					legionaryStress = battleConfig._blueStressThreshold;
					centurionStress = legionaryStress * battleConfig._blueCenturionFactor;
	 				oss << "Blue";
				}

				if(isCenturion)
				{
					oss << "Centurion_" << createdCenturions;
					createdCenturions++;
				}
				else
				{
					oss << "Legionary_" << createdLegionaries;
					createdLegionaries++;
				}

				float stressValue = legionaryStress;
				//float stressValue = Engine::GeneralState::statistics().getNormalDistValue(legionaryStress*0.5f, legionaryStress*1.5f);
				if(isCenturion)
				{
					stressValue = centurionStress;
					//stressValue = Engine::GeneralState::statistics().getNormalDistValue(centurionStress*0.5f, centurionStress*1.5f);
				}
				Legionary * legionary = new Legionary(oss.str(), isRed, stressValue);
				legionary->setCombatParams(battleConfig._killingZone, battleConfig._rangedLethality, battleConfig._closeCombatLethality);
				addAgent(legionary);
				if(isRed)
				{
					legionary->setPosition(blockPosition+warriors);
				}
				else
				{
					legionary->setPosition(blockPosition-warriors);
				}
			}
		} 
		if(isRed)
		{
			blockPosition._x += line._columns+line._separationBetweenBlocks;
		}
		else
		{
			blockPosition._x -= (line._columns+line._separationBetweenBlocks);
		}
	}
}

void Battlefield::createAgents()
{
    const BattlefieldConfig & battleConfig = (const BattlefieldConfig &)getConfig();
	
    // red a baix, blue a dalt, calculem primer el primer soldat de l'esquerra de la primera línia de combat i anem cap a darrera
	int depth = getBoundaries()._size._height/2+battleConfig._initialDistance/2;
	int redLegionaries = 0;
	int redCenturions = 0;
	for(std::list<Line>::const_iterator it=battleConfig._redLines.begin(); it!=battleConfig._redLines.end(); it++)
	{
		createLine(*it, depth, true, redLegionaries, redCenturions, battleConfig._redCenturionPosition);
		depth += (*it)._ranks+battleConfig._redSeparationBetweenLines;
	}

	depth = getBoundaries()._size._height/2-battleConfig._initialDistance/2;
	int blueLegionaries = 0;
	int blueCenturions = 0;
	for(std::list<Line>::const_iterator it=battleConfig._blueLines.begin(); it!=battleConfig._blueLines.end(); it++)
	{
		createLine(*it, depth, false, blueLegionaries, blueCenturions, battleConfig._blueCenturionPosition);
		depth -= ((*it)._ranks+battleConfig._blueSeparationBetweenLines);
	}
}

void Battlefield::stepEnvironment()
{
}

} // namespace ClassicalWarfare

