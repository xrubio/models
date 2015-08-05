
#ifndef __Legionary_hxx__
#define __Legionary_hxx__

#include <Agent.hxx>

#include <string>
#include <Point2D.hxx>
#include <typedefs.hxx>
#include <Action.hxx>

namespace ClassicalWarfare
{

class Behavior : public Engine::Action
{
	float _modifierStress;
	float _modifierRetreat;
public:
	Behavior( float modifierStress, float modifierRetreat );
	virtual ~Behavior();
	void execute( Engine::Agent & agent );
};

class Legionary : public Engine::Agent
{
protected:
	Engine::AgentsVector _enemiesAdjacent;
	Engine::AgentsVector _friendsAdjacent;
	Engine::AgentsVector _enemiesInKillingZone;
	Engine::AgentsVector _friendsInKillingZone;

	// internal state
	bool _isRed;
	// actual stress of this soldier	
	float _stress;
	// modifier that affects tension and stress depending on soldier's activity
	float _fatigueModifier;
	// true if the soldier has not thrown the pilum
	bool _pilum;

	// behavior params	
	// limit at which a soldier will try to retreat
	float _stressThreshold;
	// number of enemies killed by this Legionary
	int _kills;

	// combat params
	// distance at which a warrior can be killed
	int _killingZone;
	// default probability of killing an enemy with ranged weapons
	int _rangedLethality;
	// default probability of killing an enemy with close combat weapons
	int _closeCombatLethality;

	float _distanceToEnemy;
	
	void serialize();
	void registerAttributes();

	std::string getEnemyLegionaryType() const;
	std::string getEnemyCenturionType() const;
	std::string getFriendLegionaryType() const;
	std::string getFriendCenturionType() const;

	void casualty();
	float getFatigue() const;

	float copyStress();
	bool isBehindOf( const Engine::Agent & legionary ) const;

	bool combat(  int distance );
	// returns false if not inside
	void createInteractionLists();
	
	void increaseFatigue( float value);

public:
	// todo remove environment from here
	Legionary( const std::string & id, bool isRed, float stressThreshold);
	virtual ~Legionary();

	void setCombatParams( int killingZone, int rangedLethality, int closeCombatLethality );
	void updateKnowledge();
	void selectActions();
	void updateState();
	float getStressPercentage() const;

	void increaseStress( float stressIncrease );
	void decreaseStress( float stressDecrease);
	void advance();
	void retreat();
	void checkCombat();

	////////////////////////////////////////////////
	// This code has been automatically generated //
	/////// Please do not modify it ////////////////
	////////////////////////////////////////////////
	Legionary( void * );
	void * fillPackage();
	void sendVectorAttributes(int);
	void receiveVectorAttributes(int);
	////////////////////////////////////////////////
	//////// End of generated code /////////////////
	////////////////////////////////////////////////

};

} // namespace ClassicalWarfare

#endif // __Legionary_hxx__

