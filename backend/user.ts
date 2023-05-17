import { readFileSync } from 'fs'
import { initializeApp, cert } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'
import { hash, compare } from 'bcryptjs';
import { sign } from 'jsonwebtoken';

/* 
 * zak33, nnb28, 5/17/23: user.ts
 * 
 * Interacts with the database create users and query their high scores
 */

/** The secret key used to access our Firestore */
const serviceAccount = JSON.parse(process.env.SERVICE_ACCOUNT ?? readFileSync('./serviceAccount.json').toString());

const credential = cert(serviceAccount);

/** The Firebase app itself */
const app = initializeApp({ credential })

/** The database associated with our Firebase app */
const firestore = getFirestore(app);

/** Represents a user in Firestore */
type FirestoreUser = {
  /** The hashed password of this user */
  password: string
  /** The high score of this user */
  score: number
}

/** The collection of all 2048 userss */
const users = firestore.collection('users')

/** A user, as viewed by the API */
type User = {
  /** The username of this user */
  username: string
  /** This user's plaintext password */
  password: string
};

/**
 * Create a new user in the database
 * 
 * @param user the user to create
 */
export const createUser = async ({ username, password }: User) => {
  const userDocRef = users.doc(username)
  const userDoc = await userDocRef.get();
  if (userDoc.exists) {
    // Do not overwrite existing user
    throw new Error('User already exists');
  }
  // Create new user
  await userDocRef.set({
    password: await hash(password, 8),
    score: 0,
  })
};

/**
 * Get the high score of a user
 * 
 * @param username the user's name
 * @returns The high score of user with username `username`
 */
export const highScore = async (username: string): Promise<number> => {
  const docRef = users.doc(username);
  const userDoc = await docRef.get();
  if (!userDoc.exists) {
    // User does not exist in database
    throw new UserNotFound();
  }
  return userDoc.data().score;
}

/**
 * Get an array of ranked high scores
 * 
 * @param max The maximum number of scores to return
 * @returns At most `max` high scores
 */
export const highScores = async (max?: number): Promise<Array<{ username: string; score: number }>> => {
  // User all users in descending order of high score
  let q = users.orderBy('score', 'desc');
  if (max != null) {
    // If maximum number given, limit query
    q = q.limit(max);
  }
  // Execute query
  const { docs } = await q.get();
  return docs.map(doc => {
    const { score } = doc.data() as FirestoreUser;
    return { username: doc.id, score };
  });
}

/**
 * Set a user's high score in the database
 * 
 * @param username the username of the user
 * @param score the new high score
 * @returns a Promise that resolves when the high score is updated in Firestore
 */
export const setHighScore = async (username: string, score: number) => {
  const userDocRef = users.doc(username);
  const userDoc = await userDocRef.get();
  // User does not exist in database
  if (!userDoc.exists) throw new UserNotFound();
  // Do nothing if new score is less than current high score
  if (userDoc.data().score >= score) return;
  await userDocRef.update({ score });
}

/** Represents an error indicating that the requested user does not exist */
export class UserNotFound extends Error {
  constructor(msg?: string) {
    super(msg);
    Object.setPrototypeOf(this, UserNotFound.prototype);
  }
}

/** Represents an error indicating that an incorrect password was entered */
export class IncorrectPassword extends Error {
  constructor(msg?: string) {
    super(msg);
    Object.setPrototypeOf(this, IncorrectPassword.prototype);
  }
}

/**
 * Login to receive an access token
 * 
 * @param user the provided credentials
 * @returns An access token uniquely identiftying the user
 */
export const login = async ({ username, password }: User): Promise<string> => {
  const userDocRef = users.doc(username);
  const userDoc = await userDocRef.get();
  if (!userDoc.exists) {
    throw new UserNotFound();
  }
  const user = userDoc.data() as FirestoreUser;
  if (!await compare(password, user.password)) {
    throw new IncorrectPassword();
  }
  return sign(username, process.env.SECRET);
}


