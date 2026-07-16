/**
 * Cloud Function: setAdminRole
 * ---------------------------------------------------------------
 * Permite que un admin YA EXISTENTE asigne (o quite) el rol de
 * administrador a otro usuario, mediante un "custom claim" de
 * Firebase Auth (admin: true). Los custom claims son la forma
 * recomendada de manejar roles y se pueden leer desde las reglas
 * de Firestore (request.auth.token.admin == true).
 *
 * NO sirve para crear al PRIMER admin, porque necesita que quien
 * llama ya tenga el claim admin=true. Para crear el primer admin,
 * usa el script bootstrapAdmin.js (una sola vez, localmente).
 *
 * Despliegue:
 *   1. cd functions
 *   2. npm install firebase-admin firebase-functions
 *   3. firebase deploy --only functions
 *
 * Uso desde el cliente (una vez ya hay un admin logueado):
 *   import { getFunctions, httpsCallable } from "firebase/functions";
 *   const setAdminRole = httpsCallable(getFunctions(app), "setAdminRole");
 *   await setAdminRole({ uid: "UID_DEL_USUARIO", isAdmin: true });
 */

const { onCall, HttpsError } = require("firebase-functions/v2/https");
const { initializeApp } = require("firebase-admin/app");
const { getAuth } = require("firebase-admin/auth");

const app = initializeApp();

exports.setAdminRole = onCall(async (request) => {
  const { auth, data } = request;

  // Solo un admin existente puede llamar esta función.
  if (!auth || auth.token.admin !== true) {
    throw new HttpsError(
      "permission-denied",
      "Solo un administrador existente puede asignar el rol de admin."
    );
  }

  const { uid, isAdmin } = data;
  if (!uid || typeof uid !== "string") {
    throw new HttpsError("invalid-argument", "Falta el uid del usuario.");
  }

  await getAuth(app).setCustomUserClaims(uid, { admin: !!isAdmin });

  return { success: true, uid, admin: !!isAdmin };
});
