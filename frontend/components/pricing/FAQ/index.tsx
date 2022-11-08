import { Collapse } from "antd";
import { useColorModeValue } from '@chakra-ui/react';
import { AiOutlineCaretRight, AiOutlineCaretDown } from "react-icons/ai";

const { Panel } = Collapse;

const FAQ: React.FC = () => {
   const faqContent = [
      {
         key: 0,
         header: "Can i try before i subscribe?",
         content: `
            As a free user you have a limited access to most of our services.
            By upgrading to Premium or Gold, you get less limits and more capabilities.
         `
      },
      {
         key: 1,
         header: "What payment methods do you accept?",
         content: `
            We accept payments through Visa, MasterCard, Discover, Mobile Money and others. 
            If you don't want to use a credit card, we accept PayPal among others. 
            If you need to use any other payment method, let us know.
         `
      },
      {
         key: 2,
         header: "Can you invoice me?",
         content: `
            Yes, Invoicing is available for all the Plans. All prices are VAT included. 
            We offer monthly and annual billing. 
            You can manage your Invoices and edit your billing settings from your Account page.
         `
      },
      // {
      //    key: 3,
      //    header: "This is panel header 4",
      //    content: text
      // }
   ];
   let headingColor = useColorModeValue('rgba(0, 0, 0, 0.85)', 'slategray');

   return (
      <section className="">
         <h1 className="text-center text-2xl mt-8 mb-5" style={{color: headingColor}}>
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
