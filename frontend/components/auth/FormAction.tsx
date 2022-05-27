
type Props = {
   handleSubmit: (e: React.FormEvent<HTMLElement>) => void;
   text: string
}

const FormAction: React.FC<Props> = (props) => {
   return (
      <button
         type='submit'
         className={`
            group relative w-full flex justify-center py-2 px-4 border 
            border-transparent text-sm font-medium rounded-md text-white 
            bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 
            focus:ring-offset-2 focus:ring-blue-500 mt-10
         `}
         onSubmit={props.handleSubmit}
      >
         {props.text}
      </button>
   )
}

export default FormAction;
