
import { readFileSync } from 'fs'
import { initializeApp, cert } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'
import { hash, compare } from 'bcryptjs';
import { sign } from 'jsonwebtoken';

const serviceAccount = process.env.SERVICE_ACCOUNT ?? JSON.parse(readFileSync('./serviceAccount.json').toString());

const credential = cert(serviceAccount);

const app = initializeApp({ credential })

const firestore = getFirestore(app);

type FirestoreUser = {
  password: string
  highScore: number
}

const users = firestore.collection('users')

type User = {
  username: string
  password: string
};


export const createUser = async ({ username, password }: User) => {
  const userDocRef = users.doc(username)
  const userDoc = await userDocRef.get();
  if (userDoc.exists) {
    throw new Error('User already exists');
  }
  await userDocRef.set({
    password: await hash(password, 8),
    highScore: 0,
  })
};

export const highScore = async (username: string): Promise<number> => {
  const docRef = users.doc(username);
  const userDoc = await docRef.get();
  if (!userDoc.exists) {
    throw new Error('User not found');
  }
  return userDoc.data().highScore;
}

export const highScores = async (max?: number): Promise<Array<{ username: string; highScore: number }>> => {
  let q = users.orderBy('highScore', 'desc');
  if (max != null) {
    q = q.limit(max);
  }
  const { docs } = await q.get();
  return docs.map(doc => {
    const { highScore } = doc.data() as FirestoreUser;
    return { username: doc.id, highScore };
  });
}

export const setHighScore = async (username: string, score: number) => {
  const userDocRef = users.doc(username);
  const userDoc = await userDocRef.get();
  if (!userDoc.exists) throw new Error('User not found');
  if (userDoc.data().highScore >= score) return;
  await userDocRef.update({
    highScore: score
  });
}

export class UserNotFound extends Error {
  constructor(msg?: string) {
    super(msg);
    Object.setPrototypeOf(this, UserNotFound.prototype);
  }
}

export class IncorrectPassword extends Error {
  constructor(msg?: string) {
    super(msg);
    Object.setPrototypeOf(this, IncorrectPassword.prototype);
  }
}

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


