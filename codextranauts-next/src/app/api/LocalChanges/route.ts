import { NextResponse } from "next/server";
import { NextApiRequest } from "next";

import createClient from "@/app/services/db";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const githubId = searchParams.get("githubId");
  const githubRepo = searchParams.get("githubRepo");
  const prisma = createClient();
  const res = await prisma.user.findFirst({
    where: {
      githubId: githubId as string,
      githubRepo: githubRepo as string,
    },
    include: {
      localChanges: {
        orderBy: {
          timestamp: "desc",
        },
        take: 1,
      },
    },
  });
  const localChange = await res?.localChanges;
  return NextResponse.json(localChange);
}

export async function POST(request: Request) {
  const { username, repository, diff } = await request.json();
  const prisma = createClient();
  const githubId: string = username.toString();
  let user = await prisma.user.upsert({
    where: { githubId },
    update: {},
    create: { githubId: username, githubRepo: repository },
  });
  const localChange = await prisma.localChange.upsert({
    where: { user_id: user.id },
    update: { diff: diff },
    create: {
      user_id: user.id,
      diff: diff,
    },
  });

  return NextResponse.json({ user, localChange });
}
