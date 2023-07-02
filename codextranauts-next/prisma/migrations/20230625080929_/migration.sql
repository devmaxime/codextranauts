/*
  Warnings:

  - A unique constraint covering the columns `[user_id]` on the table `LocalChange` will be added. If there are existing duplicate values, this will fail.

*/
-- CreateIndex
CREATE UNIQUE INDEX "LocalChange_user_id_key" ON "LocalChange"("user_id");
