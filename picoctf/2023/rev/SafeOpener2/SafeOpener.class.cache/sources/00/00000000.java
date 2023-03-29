package defpackage;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Base64;

/* renamed from: SafeOpener  reason: default package */
/* loaded from: SafeOpener.class */
public class SafeOpener {
    public static void main(String[] args) throws IOException {
        BufferedReader keyboard = new BufferedReader(new InputStreamReader(System.in));
        Base64.Encoder encoder = Base64.getEncoder();
        for (int i = 0; i < 3; i++) {
            System.out.print("Enter password for the safe: ");
            String key = keyboard.readLine();
            String encodedkey = encoder.encodeToString(key.getBytes());
            System.out.println(encodedkey);
            boolean isOpen = openSafe(encodedkey);
            if (!isOpen) {
                System.out.println("You have  " + (2 - i) + " attempt(s) left");
            } else {
                return;
            }
        }
    }

    public static boolean openSafe(String password) {
        if (password.equals("picoCTF{SAf3_0p3n3rr_y0u_solv3d_it_de45efd6}")) {
            System.out.println("Sesame open");
            return true;
        }
        System.out.println("Password is incorrect\n");
        return false;
    }
}