/*
  Warnings:

  - A unique constraint covering the columns `[githubId]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[githubRepo]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `githubId` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `githubRepo` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "User" ADD COLUMN     "githubId" TEXT NOT NULL,
ADD COLUMN     "githubRepo" TEXT NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "User_githubId_key" ON "User"("githubId");

-- CreateIndex
CREATE UNIQUE INDEX "User_githubRepo_key" ON "User"("githubRepo");
