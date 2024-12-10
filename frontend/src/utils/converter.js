import { comparison } from "../mock/docs";

export function renameFile(file, title) {
  console.log("Title: " + title);
  const arrExtension = file.name.split(".");
  const extension = arrExtension[arrExtension.length - 1];
  const newFile = new File([file], `${comparison[title]}.${extension}`, {
    type: file.type,
  });
  return newFile;
}

export function renameFileStatement(file, index) {
  const arrExtension = file.name.split(".");
  const extension = arrExtension[arrExtension.length - 1];
  const newFile = new File([file], `bank_reference${index}.${extension}`, {
    type: file.type,
  });
  return newFile;
}

export function renameFileCheck(file, index) {
  const arrExtension = file.name.split(".");
  const extension = arrExtension[arrExtension.length - 1];
  const newFile = new File([file], `cheque${index}.${extension}`, {
    type: file.type,
  });
  return newFile;
}
