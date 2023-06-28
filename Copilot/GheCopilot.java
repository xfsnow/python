import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

import org.json.JSONObject;

public class GheCopilot {
    public static void main(String[] args) throws IOException {
        String token = args[0];
        String username = args[1];
        String email = args[2];
        createUser(token, username, email);
    }

public static void createUser(String token, String username, String email) throws IOException {
        String url = "https://api.github.com/admin/users";
        String payload = "{\n" +
                "    \"login\": \"" + username + "\",\n" +
                "    \"email\": \"" + email + "\",\n" +
                "    \"name\": \"" + username + "\",\n" +
                "    \"active\": true,\n" +
                "    \"private\": false,\n" +
                "    \"restricted\": false,\n" +
                "    \"allow_squash_merge\": true,\n" +
                "    \"allow_merge_commit\": true,\n" +
                "    \"allow_rebase_merge\": true,\n" +
                "    \"allow_auto_merge\": false,\n" +
                "    \"two_factor_requirement_enabled\": false,\n" +
                "    \"user_type\": \"user\",\n" +
                "    \"owned_private_repos\": 0,\n" +
                "    \"plan\": {\n" +
                "        \"name\": \"free\",\n" +
                "        \"private_repos\": 0,\n" +
                "        \"space\": 976562499,\n" +
                "        \"collaborators\": 0\n" +
                "    }\n" +
                "}";
        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Authorization", "Bearer " + token);
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);
        con.getOutputStream().write(payload.getBytes("UTF-8"));
        int responseCode = con.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_CREATED) {
            System.out.println("User created successfully.");
        } else {
            System.out.println("Failed to create user. Response code: " + responseCode);
            Scanner scanner = new Scanner(con.getErrorStream());
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
            scanner.close();
        }
    }

    public static void enableCopilot(String token, String username) throws IOException {
        String url = "https://api.github.com/users/" + username + "/interaction-limits";
        JSONObject payload = new JSONObject();
        payload.put("limit", "unlimited");
        payload.put("origin", "cli");
        URL obj = new URL(url);
        HttpURLConnection con = (HttpURLConnection) obj.openConnection();
        con.setRequestMethod("PUT");
        con.setRequestProperty("Authorization", "token " + token);
        con.setRequestProperty("Content-Type", "application/json");
        con.setRequestProperty("Accept", "application/vnd.github.sombra-preview+json");
        con.setDoOutput(true);
        con.getOutputStream().write(payload.toString().getBytes("UTF-8"));
        int responseCode = con.getResponseCode();
        if (responseCode == HttpURLConnection.HTTP_OK) {
            System.out.println("User GitHub Copilot enabled successfully!");
        } else {
            System.out.println("User GitHub Copilot enabled failed!");
            Scanner scanner = new Scanner(con.getErrorStream());
            while (scanner.hasNextLine()) {
                System.out.println(scanner.nextLine());
            }
            scanner.close();
        }
    }
}