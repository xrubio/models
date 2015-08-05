
#include "Legionary.hxx"

#include <Exception.hxx>
#include <cstring>
#include <Statistics.hxx>
#include <GeneralState.hxx>
#include "Battlefield.hxx"
#include <typedefs.hxx>

namespace ClassicalWarfare
{

Behavior::Behavior( float modifierStress, float modifierRetreat ) : _modifierStress(modifierStress), _modifierRetreat(modifierRetreat)
{
}

Behavior::~Behavior()
{
}

void Behavior::execute( Engine::Agent & agent )
{
	// stress
	Legionary & legionary = (Legionary &)agent;
	if(_modifierStress>0.0f)
	{
		legionary.increaseStress(_modifierStress);
	}
	else
	{
		legionary.decreaseStress(-_modifierStress);
	}
	// advance/retreat
	if(_modifierRetreat>0.9f)
	{
		legionary.advance();
	}
	else if(_modifierRetreat<0.1f)
	{
		legionary.retreat();
	}
	// combat
	legionary.checkCombat();
}

Legionary::Legionary( const std::string & id, bool isRed, float stressThreshold) : Agent(id), _isRed(isRed), _stress(0.0f), _fatigueModifier(1.0f), _pilum(true), _stressThreshold(stressThreshold), _kills(0)
{
}

Legionary::~Legionary()
{
}
	
void Legionary::setCombatParams( int killingZone, int rangedLethality, int closeCombatLethality )
{
	_killingZone = killingZone;
	_rangedLethality = rangedLethality;
	_closeCombatLethality = closeCombatLethality;
}

void Legionary::casualty()
{
	for(Engine::AgentsVector::iterator it=_friendsInKillingZone.begin(); it!=_friendsInKillingZone.end(); it++)
	{
        Legionary * agent = (Legionary*)(it->get());
		float maxValue = 0.1f;
		float distance = agent->getPosition().distance(_position);
		maxValue = maxValue * pow(exp(1.0f), -0.5*(distance-1.0f));
		agent->increaseFatigue(maxValue);
		agent->increaseStress(maxValue);
	}
	remove();
}

void Legionary::increaseFatigue( float value)
{
	_fatigueModifier = _fatigueModifier+value;
}

void Legionary::increaseStress( float stressIncrease )
{
	_stress += stressIncrease*_fatigueModifier;
	_stress = std::min(2.0f*_stressThreshold, _stress);
}

void Legionary::decreaseStress( float stressDecrease )
{
	_stress -= stressDecrease/_fatigueModifier;
	_stress = std::max(0.0f, _stress);
}

std::string Legionary::getFriendLegionaryType() const
{
	std::string type = getType();
	std::string side = "Red";
	if(type.compare(0, side.length(), side)==0)
	{
		return "RedLegionary";
	}
	return "BlueLegionary";
}

std::string Legionary::getFriendCenturionType() const
{
	std::string type = getType();
	std::string side = "Red";
	if(type.compare(0, side.length(), side)==0)
	{
		return "RedCenturion";
	}
	return "BlueCenturion";
}

std::string Legionary::getEnemyLegionaryType() const
{
	std::string type = getType();
	std::string side = "Red";
	if(type.compare(0, side.length(), side)==0)
	{
		return "BlueLegionary";
	}
	return "RedLegionary";
}

std::string Legionary::getEnemyCenturionType() const
{
	std::string type = getType();
	std::string side = "Red";
	if(type.compare(0, side.length(), side)==0)
	{
		return "BlueCenturion";
	}
	return "RedCenturion";
}

void Legionary::advance()
{
	Engine::Point2D<int> newPosition(_position._x, _position._y+1);		
	if(_isRed)
	{
		newPosition._y = _position._y-1;
	}

	if(_world->checkPosition(newPosition) && _world->getAgent(newPosition).size()==0)
	{
		setPosition(newPosition);
	}
}

void Legionary::retreat()
{
	Engine::Point2D<int> newPosition(_position._x, _position._y-1);		
	if(_isRed)
	{
		newPosition._y = _position._y+1;
	}	
	if(_world->checkPosition(newPosition))
	{
		if(_world->getAgent(newPosition).size()==0)
		{
			setPosition(newPosition);
			return;
		}
	}
	else
	{
		// remove from simulation
		setExists(false);
	}
}

void Legionary::checkCombat()
{
	if(_pilum && _enemiesInKillingZone.size()!=0)
	{
		int index = Engine::GeneralState::statistics().getUniformDistValue(0, 10);
		if(index==0)
		{
			_pilum = false;
			combat(_killingZone);
		}
	}
	if(_enemiesAdjacent.size()!=0)
	{
		combat(1);
	}
}

bool Legionary::combat( int distance )
{
	Legionary * enemy = 0;
	if(distance==1)
	{
		// randomly choose an enemy
		int index = Engine::GeneralState::statistics().getUniformDistValue(0, _enemiesAdjacent.size()-1);
		enemy = (Legionary*)(_enemiesAdjacent.at(index).get());
		float probKilled = _closeCombatLethality*enemy->getStressPercentage();
		// cubic increase
		probKilled = pow(probKilled, 3.0f);
		int value = Engine::GeneralState::statistics().getUniformDistValue(0,999);
		if(value>=probKilled)
		{
			return false;
		}
	}
	else
	{
		int value = Engine::GeneralState::statistics().getUniformDistValue(0,999);
		// ranged lethality%
		if(value>=_rangedLethality)
		{
			return false;
		}
		int index = Engine::GeneralState::statistics().getUniformDistValue(0, _enemiesInKillingZone.size()-1);
		enemy = (Legionary*)(_enemiesInKillingZone.at(index).get());
	}
	//std::cout << "enemy: " << enemy << " with stress percentage: " << enemy->getStressPercentage() << " killed at step: " << _world->getCurrentStep() << " and range: " << distance << std::endl;
	enemy->setExists(false);
	if(distance>1)
	{
		// enemy blue
		if(_isRed)
		{
			_world->setValue(eBlueRanged, enemy->getPosition(), 1+_world->getValue(eBlueRanged, enemy->getPosition()));
		}
		else
		{
			_world->setValue(eRedRanged, enemy->getPosition(), 1+_world->getValue(eRedRanged, enemy->getPosition()));
		}
	}
	else
	{
		// enemy blue
		if(_isRed)
		{
			_world->setValue(eBlueCloseCombat, enemy->getPosition(), 1+_world->getValue(eBlueCloseCombat, enemy->getPosition()));
		}
		else
		{
			_world->setValue(eRedCloseCombat, enemy->getPosition(), 1+_world->getValue(eRedCloseCombat, enemy->getPosition()));
		}
	}
	_kills++;
	return true;
}

void Legionary::createInteractionLists()
{
	_enemiesAdjacent.clear();
	_friendsAdjacent.clear();
	_friendsInKillingZone.clear();
	_enemiesInKillingZone.clear();

	Engine::AgentsVector agents = _world->getNeighbours(this, _killingZone);
	_distanceToEnemy = std::numeric_limits<float>::max();
	for(Engine::AgentsVector::iterator it=agents.begin(); it!=agents.end(); it++)
	{
        Engine::AgentPtr agent = *it;	
		if(agent->isType(getEnemyLegionaryType()) || agent->isType(getEnemyCenturionType()))
		{
			float distance = agent->getPosition().distance(_position);
			if(distance<_distanceToEnemy)
			{
				_distanceToEnemy = distance;
			}
			_enemiesInKillingZone.push_back(agent);		
			// < 1.44 is distance to diagonal so...
			if(distance<1.5f)
			{
				_enemiesAdjacent.push_back(agent);
			}
		}
		// friends in front
		else
		{
			float distance = agent->getPosition().distance(_position);
			// < 1.44 is distance to diagonal so...
			if(distance<1.5f)
			{
				_friendsAdjacent.push_back(agent);
			}
			_friendsInKillingZone.push_back(agent);
		}
	}
	_distanceToEnemy = std::min(float(2.0f*_killingZone), _distanceToEnemy);
}

bool Legionary::isBehindOf( const Engine::Agent & legionary ) const
{
	if(_isRed)
	{
		if(legionary.getPosition()._y<_position._y)
		{
			return true;
		}
		return false;
	}
	else
	{	
		if(legionary.getPosition()._y>_position._y)
		{
			return true;
		}
		return false;
	}
}

float Legionary::getFatigue() const
{
	return _fatigueModifier;
}

float Legionary::copyStress()
{
    Engine::AgentsVector forwardLegionaries;
	
	for(Engine::AgentsVector::const_iterator it=_friendsAdjacent.begin(); it!=_friendsAdjacent.end(); it++)
	{
        Legionary * legionary = (Legionary*)(it->get());
		if(!legionary->isBehindOf(*this))
		{
			forwardLegionaries.push_back(*it);
			continue;
		}
	}
	float diff = 0.0f;
	if(forwardLegionaries.size()!=0)
	{
		int index = Engine::GeneralState::statistics().getUniformDistValue(0, forwardLegionaries.size()-1);
        Legionary * legionary = (Legionary*)(forwardLegionaries.at(index).get());
		float finalStress = legionary->getStressPercentage()*_stressThreshold;
		diff = finalStress-_stress;
	}
	return diff;
}

void Legionary::updateKnowledge()
{
	createInteractionLists();	
}

void Legionary::selectActions()
{
	float modifierStress = copyStress();

	float modifRetreat = getStressPercentage();
	modifRetreat = modifRetreat*12.0f;
	modifRetreat-= 6.0f;
	float modifierRetreat = 1.0f/(1+pow(exp(1), modifRetreat));

	// modif: 0 if dist to enemy = 0, 1 if dist to enemy = Kz, adjusted from -6 to 6
	float modif = _stressThreshold*_distanceToEnemy/float(_killingZone);
	modif = modif*12.0f;
	modif -= 6.0f;
	// move between -6 and 6 for logistic function
	modifierStress += 0.1f/(1+pow(exp(1), modif))-0.05f;

	_actions.push_back(new Behavior(modifierStress, modifierRetreat));
}

void Legionary::updateState()
{
	if(!_exists)
	{
		casualty();
	}
}

void Legionary::serialize()
{
	serializeAttribute("stress x100", int(_stress*100.0f)); 
	serializeAttribute("stress threshold x100", int(_stressThreshold*100.0f)); 
	serializeAttribute("pilum", int(_pilum));
//	serializeAttribute("fatigue modif x100", int(_fatigueModifier*100.0f)); 
//	serializeAttribute("dist enemy", _distanceToEnemy);
//	serializeAttribute("stress percentage", int(getStressPercentage()*100.0f));
	serializeAttribute("kills", _kills);
}

void Legionary::registerAttributes()
{
	registerIntAttribute("stress x100");
	registerIntAttribute("stress threshold x100");
	registerIntAttribute("pilum");
//	registerIntAttribute("fatigue modif x100");
//	registerIntAttribute("dist enemy");
//	registerIntAttribute("stress percentage");
	registerIntAttribute("kills");
}

float Legionary::getStressPercentage() const
{
	return _stress/_stressThreshold;
}

} // namespace ClassicalWarfare

