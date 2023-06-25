-- CreateTable
CREATE TABLE "User" (
    "id" SERIAL NOT NULL,

    CONSTRAINT "User_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "LocalChange" (
    "id" SERIAL NOT NULL,
    "user_id" INTEGER NOT NULL,
    "diff" TEXT NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "LocalChange_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "LocalChange" ADD CONSTRAINT "LocalChange_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
