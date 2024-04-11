import React, { memo, useContext, useEffect, useState } from "react";
import roleContext from "../contexts/roleContext";
import DocViewer, { DocViewerRenderers } from "@cyntler/react-doc-viewer";
import { OutTable } from "react-excel-renderer";

const DocumentView = ({ foo }) => {
  const contextFiles = useContext(roleContext);
  const [pdfURL, setPdfURL] = useState();

  useEffect(() => {
    setPdfURL(contextFiles?.pdfURL);
  }, [contextFiles?.pdfURL]);

  return (
    <div
      className={`bg-[#FFFFFF] h-[calc(100vh-93px)] overflow-auto scrollbarCustom px-3 `}
      // scrollbar - remove scrollbar
    >
      {pdfURL ? (
        pdfURL?.rows && pdfURL?.cols ? (
          <OutTable
            data={pdfURL?.rows || []}
            columns={pdfURL?.cols || []}
            tableClassName="ExcelTable2007 border"
            tableHeaderRowClass="font-bold bg-blue-100"
          />
        ) : (
          <DocViewer
            pluginRenderers={DocViewerRenderers}
            documents={[{ uri: pdfURL }]}
            config={{
              header: {
                disableHeader: true,
                disableFileName: false,
                retainURLParams: false,
              },
              pdfVerticalScrollByDefault: true,
              loadingRenderer: {
                overrideComponent: () => {
                  console.log("Loading...");
                  return <div>Loading Custom</div>;
                },
                showLoadingTimeout: true,
              },
              noRenderer: {
                overrideComponent: ({ document }) => {
                  return (
                    <div className="flex justify-center items-center w-full">
                      Error:{" "}
                      {document?.fileType?.includes("webp")
                        ? "Webp file not supported"
                        : "Something went wrong"}
                    </div>
                  );
                },
              },
            }}
          />
        )
      ) : null}
    </div>
  );
};

export default memo(DocumentView);
