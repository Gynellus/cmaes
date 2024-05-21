import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

import com.google.gson.Gson;

import engine.core.MarioGame;
import engine.core.MarioResult;
import engine.core.MarioResultDTO;



public class PlayLevel {
    public static void printResults(MarioResult result) {
        System.out.println("****************************************************************");
        System.out.println("Game Status: " + result.getGameStatus().toString() +
                " Percentage Completion: " + result.getCompletionPercentage());
        System.out.println("Lives: " + result.getCurrentLives() + " Coins: " + result.getCurrentCoins() +
                " Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f));
        System.out.println("Mario State: " + result.getMarioMode() +
                " (Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: " + result.getNumCollectedFireflower() + ")");
        System.out.println("Total Kills: " + result.getKillsTotal() + " (Stomps: " + result.getKillsByStomp() +
                " Fireballs: " + result.getKillsByFire() + " Shells: " + result.getKillsByShell() +
                " Falls: " + result.getKillsByFall() + ")");
        System.out.println("Bricks: " + result.getNumDestroyedBricks() + " Jumps: " + result.getNumJumps() +
                " Max X Jump: " + result.getMaxXJump() + " Max Air Time: " + result.getMaxJumpAirTime());
        System.out.println("****************************************************************");
    }

    public static String getLevel(String filepath) {
        String content = "";
        try {
            content = new String(Files.readAllBytes(Paths.get(filepath)));
        } catch (IOException e) {
        }
        return content;
    }

    public static String resultsToJson(MarioResult result) {
        MarioResultDTO dto = new MarioResultDTO(result);
        Gson gson = new Gson();
        return gson.toJson(dto);
    }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java PlayLevel <levelPath> [<timer> <MarioState> <visuals>]");
            return;
        }
        
        // Level path is required
        String levelPath = args[0];
    
        // Default values
        int timer = 20;
        int marioState = 0;
        boolean visuals = false;
    
        // Override default values if additional arguments are provided
        if (args.length > 1 && args[1] != null) {
            try {
                timer = Integer.parseInt(args[1]);
            } catch (NumberFormatException e) {
                System.out.println("Invalid format for timer, using default: " + timer);
            }
        }
        if (args.length > 2 && args[2] != null) {
            try {
                marioState = Integer.parseInt(args[2]);
            } catch (NumberFormatException e) {
                System.out.println("Invalid format for Mario state, using default: " + marioState);
            }
        }
        if (args.length > 3 && args[3] != null) {
            visuals = Boolean.parseBoolean(args[3]);
        }
    
        MarioGame game = new MarioGame();
        MarioResult result = game.runGame(new agents.robinBaumgarten.Agent(), getLevel(levelPath), timer, marioState, visuals);
        printResults(result);
        String jsonResults = resultsToJson(result);
        System.out.println(jsonResults);
    }
    
}
