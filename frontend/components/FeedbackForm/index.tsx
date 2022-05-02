import { Form, Input, Button, Popover } from 'antd';

const { TextArea } = Input;

const FeedbackForm: React.FunctionComponent = () => {
   const validateMessages = {
      required: '${label} is required!',
      types: {
         email: '${label} is not a valid email!',
      },
   };

   const handleFormSuccess = (values: any) => {
      console.log(values);
   }

   const handleFormFailed = ({ values, errorFields, outOfDate }: any) => {
      console.log(values);
      console.log(errorFields);
      console.log(outOfDate);
   }

   const content = (
      <Form 
         onFinish={handleFormSuccess} 
         onFinishFailed={handleFormFailed} 
         validateMessages={validateMessages} 
         layout="vertical"
      >
         <Form.Item required name="email" label="Email" rules={[{ required: true }]}>
            <Input placeholder="Your email address" type="email" />
         </Form.Item>
         <Form.Item required name="feedback" label="Feedback" rules={[{ required: true }]}>
            <TextArea rows={4} cols={25} maxLength={500} placeholder="Your feedback..." />
         </Form.Item>
         <Form.Item>
            <Button type="primary" htmlType="submit">Send</Button>
         </Form.Item>
      </Form>
   );

   return (
      <div className="container">
         <Popover 
            content={content} 
            trigger="click" 
            title={
               <p className="text-center pt-5">
                  Share any feedback about our services
               </p>
            }
         >
            <Button>Feedback</Button>
         </Popover>
      </div>
   );
}


export default FeedbackForm;
