-- Guild emblems of up to 256x256 pixels (BMP, GIF or PNG) can exceed a blob's 64 KB
ALTER TABLE `guild_emblems` MODIFY `file_data` mediumblob;
