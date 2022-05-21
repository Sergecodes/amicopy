import { Collapse } from "antd";
import { AiOutlineCaretRight, AiOutlineCaretDown } from "react-icons/ai";

const { Panel } = Collapse;

const FAQ: React.FunctionComponent = () => {
   const text = `
    A dog is a type of domesticated animal.
    Known for its loyalty and faithfulness,
    it can be found as a welcome guest in many households across the world.
  `;

   const faqContent = [
      {
         key: 0,
         header: "This is panel header 1",
         content: text
      },
      {
         key: 1,
         header: "This is panel header 2",
         content: text
      },
      {
         key: 2,
         header: "This is panel header 3",
         content: text
      },
      {
         key: 3,
         header: "This is panel header 4",
         content: text
      }
   ];

   return (
      <section className="">
         <h1 className="text-center text-2xl mt-8 mb-5">
            Frequently Asked Questions
         </h1>
         <Collapse
            accordion
            bordered={false}
            defaultActiveKey={["1"]}
            expandIcon={({ isActive }) =>
               isActive ? <AiOutlineCaretDown /> : <AiOutlineCaretRight />
            }
         >
            {faqContent.map((obj) => (
               <Panel header={obj.header} key={obj.key} className="panelCollapse">
                  <p>{obj.content}</p>
               </Panel>
            ))}
         </Collapse>

         <style jsx>{`
            .panelCollapse {
               margin-bottom: 24px;
               overflow: hidden;
               background: #f7f7f7;
               border: 0px;
               border-radius: 2px;
            }
         `}</style>
      </section>
   );
};

export default FAQ;
