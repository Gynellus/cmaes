package engine.core;
import engine.helper.GameStatus;

// This class is used to serialize the MarioResult object to JSON
public class MarioResultDTO {
    private GameStatus gameStatus;
    private float completionPercentage;
    private int remainingTime;
    private int marioMode;
    private int currentLives;
    private int currentCoins;
    private int totalKills;
    private int killsByStomp;
    private int killsByFire;
    private int killsByShell;
    private int killsByFall;
    private int numDestroyedBricks;
    private int numJumps;
    private float maxXJump;
    private int maxJumpAirTime;

    // Constructor
    public MarioResultDTO(MarioResult result) {
        this.gameStatus = result.getGameStatus();
        this.completionPercentage = result.getCompletionPercentage();
        this.remainingTime = result.getRemainingTime();
        this.marioMode = result.getMarioMode();
        this.currentLives = result.getCurrentLives();
        this.currentCoins = result.getCurrentCoins();
        this.totalKills = result.getKillsTotal();
        this.killsByStomp = result.getKillsByStomp();
        this.killsByFire = result.getKillsByFire();
        this.killsByShell = result.getKillsByShell();
        this.killsByFall = result.getKillsByFall();
        this.numDestroyedBricks = result.getNumDestroyedBricks();
        this.numJumps = result.getNumJumps();
        this.maxXJump = result.getMaxXJump();
        this.maxJumpAirTime = result.getMaxJumpAirTime();
    }

    // Getters
    public GameStatus getGameStatus() { return gameStatus; }
    public float getCompletionPercentage() { return completionPercentage; }
    public int getRemainingTime() { return remainingTime; }
    public int getMarioMode() { return marioMode; }
    public int getCurrentLives() { return currentLives; }
    public int getCurrentCoins() { return currentCoins; }
    public int getTotalKills() { return totalKills; }
    public int getKillsByStomp() { return killsByStomp; }
    public int getKillsByFire() { return killsByFire; }
    public int getKillsByShell() { return killsByShell; }
    public int getKillsByFall() { return killsByFall; }
    public int getNumDestroyedBricks() { return numDestroyedBricks; }
    public int getNumJumps() { return numJumps; }
    public float getMaxXJump() { return maxXJump; }
    public int getMaxJumpAirTime() { return maxJumpAirTime; }
}
